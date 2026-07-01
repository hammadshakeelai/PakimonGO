import 'package:flutter/material.dart';
import 'package:mapbox_maps_flutter/mapbox_maps_flutter.dart';

import '../../../core/config/app_config.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  @override
  Widget build(BuildContext context) {
    if (!AppConfig.hasMapboxToken) {
      return Scaffold(
        appBar: AppBar(title: const Text('PakimonGO Map')),
        body: const Center(
          child: Text(
            'Map unavailable — set MAPBOX_ACCESS_TOKEN',
            style: TextStyle(color: Colors.grey),
          ),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(title: const Text('PakimonGO Map')),
      body: MapWidget(
        styleUri: MapboxStyles.MAPBOX_STREETS,
        viewport: CameraViewportState(
          center: Point(coordinates: Position(0, 0)),
          zoom: 2.0,
        ),
      ),
    );
  }
}
