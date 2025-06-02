<template>
  <div class="route-info-container">
    <div v-if="routePath" class="delivery-info">
      <div class="info-item">
        <span class="info-label">预计送达时间：</span>
        <span class="info-value">{{ formatDuration(routePath.duration) }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">预计距离：</span>
        <span class="info-value">{{ formatDistance(routePath.distance) }}</span>
      </div>
    </div>
    
    <!-- 地图容器 -->
    <div ref="mapContainer" class="route-map-container"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, computed } from 'vue';
import { message } from 'ant-design-vue';

const props = defineProps({
  origin: {
    type: Object,
    default: null,
    validator: (value) => !value || (value && typeof value.lat === 'number' && typeof value.lng === 'number'),
  },
  destination: {
    type: Object,
    default: null,
    validator: (value) => !value || (value && typeof value.lat === 'number' && typeof value.lng === 'number'),
  },
  routePath: {
    type: Object,
    default: null,
  },
});

const mapContainer = ref(null);
let mapInstance = null;
let routePolyline = null;
let startMarker = null;
let endMarker = null;

// 高德地图 JS API Key (前端公开密钥)
const AMAP_JS_API_KEY = 'ac47d45ec5e5e8ddf58b95e9e99ede62';
const AMAP_SECURITY_JS_CODE = 'ac47d45ec5e5e8ddf58b95e9e99ede62';

const loadAmapScript = () => {
  return new Promise((resolve, reject) => {
    if (window.AMap) {
      resolve(window.AMap);
      return;
    }
    window._AMapSecurityConfig = {
      securityJsCode: AMAP_SECURITY_JS_CODE,
    };
    const script = document.createElement('script');
    // Load only core map, Marker, Polyline. Driving plugin not directly used for search here.
    script.src = `https://webapi.amap.com/maps?v=2.0&key=${AMAP_JS_API_KEY}&plugin=AMap.Marker,AMap.Polyline`;
    script.onload = () => {
      if (window.AMap) {
        resolve(window.AMap);
      } else {
        reject(new Error('高德地图脚本加载失败'));
      }
    };
    script.onerror = (err) => {
      reject(new Error(`高德地图脚本加载失败: ${err.message}`));
    };
    document.head.appendChild(script);
  });
};

// 保留时间和距离格式化函数
const formatDuration = (seconds) => {
  if (!seconds) return '--';
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  
  if (hours > 0) {
    return `${hours}小时${minutes}分钟`;
  } else {
    return `${minutes}分钟`;
  }
};

const formatDistance = (meters) => {
  if (!meters) return '--';
  if (meters >= 1000) {
    return `${(meters / 1000).toFixed(1)}公里`;
  } else {
    return `${meters}米`;
  }
};

const initMap = async () => {
  if (!mapContainer.value) {
    console.error('地图容器未找到');
    message.error('地图容器加载失败');
    return;
  }

  try {
    const AMap = await loadAmapScript();
    if (!AMap) {
      message.error('高德地图服务加载失败');
      return;
    }

    // 默认显示北京市中心，如果有起点终点则显示中心点
    let center = [116.397428, 39.90923]; // 北京市中心
    let zoom = 10;

    if (props.origin && props.destination) {
      center = [
        (props.origin.lng + props.destination.lng) / 2,
        (props.origin.lat + props.destination.lat) / 2,
      ];
      zoom = 12;
    } else if (props.origin) {
      center = [props.origin.lng, props.origin.lat];
      zoom = 15;
    } else if (props.destination) {
      center = [props.destination.lng, props.destination.lat];
      zoom = 15;
    }

    mapInstance = new AMap.Map(mapContainer.value, {
      zoom: zoom,
      center: center,
      resizeEnable: true,
    });

    mapInstance.on('complete', () => {
      console.log('地图加载完成 (RouteMap.vue)');
      drawRouteAndMarkers();
    });

    mapInstance.on('error', (e) => {
      console.error('地图加载错误 (RouteMap.vue):', e);
      message.error('地图组件发生错误，请稍后重试');
    });

  } catch (error) {
    console.error('初始化地图失败 (RouteMap.vue):', error);
    message.error(`地图初始化失败: ${error.message}`);
  }
};

const clearMapElements = () => {
  if (routePolyline) {
    mapInstance.remove(routePolyline);
    routePolyline = null;
  }
  if (startMarker) {
    mapInstance.remove(startMarker);
    startMarker = null;
  }
  if (endMarker) {
    mapInstance.remove(endMarker);
    endMarker = null;
  }
};

const drawRouteAndMarkers = () => {
  if (!mapInstance || !window.AMap) {
    console.warn('地图服务尚未准备好 (RouteMap.vue)');
    return;
  }
  const AMap = window.AMap;

  clearMapElements();

  // Draw Markers with different icons and clear labels
  if (props.origin) {
    startMarker = new AMap.Marker({
      position: new AMap.LngLat(props.origin.lng, props.origin.lat),
      // 使用绿色标记表示起点
      icon: 'https://webapi.amap.com/theme/v1.3/markers/n/start.png',
      offset: new AMap.Pixel(-9, -31),
      title: '起点',
    });
    mapInstance.add(startMarker);
  }

  if (props.destination) {
    endMarker = new AMap.Marker({
      position: new AMap.LngLat(props.destination.lng, props.destination.lat),
      // 使用红色标记表示终点
      icon: 'https://webapi.amap.com/theme/v1.3/markers/n/end.png',
      offset: new AMap.Pixel(-9, -31),
      title: '终点',
    });
    mapInstance.add(endMarker);
  }
    // Draw Polyline from routePath
  if (props.routePath && props.routePath.steps && props.routePath.steps.length > 0) {
    const pathCoords = [];
    
    props.routePath.steps.forEach(step => {
      if (step.polyline && step.polyline.length > 0) {
        // 高德地图API返回的polyline格式：经度,纬度;经度,纬度;...
        const polylinePoints = step.polyline.split(';');
        polylinePoints.forEach(pointStr => {
          if (pointStr.includes(',')) {
            const [lng, lat] = pointStr.split(',');
            const lngNum = parseFloat(lng);
            const latNum = parseFloat(lat);
            if (!isNaN(lngNum) && !isNaN(latNum)) {
              pathCoords.push(new AMap.LngLat(lngNum, latNum));
            }
          }
        });
      }
    });

    if (pathCoords.length > 0) {
      routePolyline = new AMap.Polyline({
        path: pathCoords,
        borderWeight: 2,
        strokeColor: '#0091ff', // Blue color for the route
        strokeOpacity: 0.8,
        strokeWeight: 6,
        lineJoin: 'round',
        lineCap: 'round',
      });
      mapInstance.add(routePolyline);
      mapInstance.setFitView([startMarker, endMarker, routePolyline], false, [60, 60, 60, 60]); // Adjust padding as needed
    } else {
       if (startMarker && endMarker) mapInstance.setFitView([startMarker, endMarker]);
    }
  } else {
    // If no route path, just fit markers
    if (startMarker && endMarker) {
      mapInstance.setFitView([startMarker, endMarker]);
    } else if (startMarker) {
      mapInstance.setCenter(startMarker.getPosition());
      mapInstance.setZoom(15);
    } else if (endMarker) {
      mapInstance.setCenter(endMarker.getPosition());
      mapInstance.setZoom(15);
    }
  }
};

onMounted(async () => {
  await nextTick();
  // 无论是否有起点终点都初始化地图
  initMap();
});

watch(
  () => [props.origin, props.destination],
  async ([newOrigin, newDest], [oldOrigin, oldDest]) => {
    if (!mapInstance) {
      await nextTick();
      initMap();
      return;
    }
    
    // 根据新的起点终点更新地图中心
    if (newOrigin && newDest) {
      mapInstance.setCenter([
        (newOrigin.lng + newDest.lng) / 2,
        (newOrigin.lat + newDest.lat) / 2,
      ]);
      mapInstance.setZoom(12);
    } else if (newOrigin) {
      mapInstance.setCenter([newOrigin.lng, newOrigin.lat]);
      mapInstance.setZoom(15);
    } else if (newDest) {
      mapInstance.setCenter([newDest.lng, newDest.lat]);
      mapInstance.setZoom(15);
    }
    
    if (!props.routePath) {
      drawRouteAndMarkers();
    }
  },
  { deep: true }
);

watch(
  () => props.routePath,
  (newRoutePath, oldRoutePath) => {
    if (mapInstance) {
      if (newRoutePath) {
        console.log('RoutePath changed, redrawing route:', newRoutePath);
        drawRouteAndMarkers();
      } else if (oldRoutePath && !newRoutePath) {
        console.log('RoutePath cleared, clearing polyline and fitting markers.');
        drawRouteAndMarkers();
      }
    }
  },
  { deep: true, immediate: true }
);

</script>

<style scoped>
.route-info-container {
  width: 100%;
  border: 1px solid #d9d9d9;
  border-radius: 8px;
  overflow: hidden;
}

.delivery-info {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  gap: 16px; /* 增加间距，因为现在只有两个项目 */
}

.info-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 100px; /* 增加最小宽度，因为现在只有两个项目 */
}

.info-label {
  font-size: 12px;
  opacity: 0.9;
  margin-bottom: 4px;
}

.info-value {
  font-size: 14px;
  font-weight: 600;
}

.route-map-container {
  width: 100%;
  height: 300px; 
  border: none;
}

@media (max-width: 768px) {
  .delivery-info {
    padding: 12px;
    flex-direction: column;
    gap: 8px;
  }
  
  .info-item {
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
    min-width: auto;
  }
  
  .info-label {
    margin-bottom: 0;
    margin-right: 8px;
  }
}
</style>
