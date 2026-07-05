import 'package:flutter/material.dart';
import 'package:mapbox_maps_flutter/mapbox_maps_flutter.dart';

import '../../../core/config/app_config.dart';
import '../../../shared/widgets/error_retry_view.dart';
import '../../capture/data/capture_repository.dart';
import '../domain/map_viewmodel.dart';
import 'marker_list_screen.dart';

class MapScreen extends StatefulWidget {
  final MapViewModel? viewModel;

  const MapScreen({super.key, this.viewModel});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  late final MapViewModel _viewModel;

  @override
  void initState() {
    super.initState();
    _viewModel = widget.viewModel ?? _createDefaultViewModel();
    _viewModel.addListener(_onViewModelChanged);
    _viewModel.fetchMarkers();
  }

  MapViewModel _createDefaultViewModel() {
    return MapViewModel(
      repository: CaptureRepository(),
    );
  }

  @override
  void dispose() {
    _viewModel.removeListener(_onViewModelChanged);
    _viewModel.dispose();
    super.dispose();
  }

  void _onViewModelChanged() {
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('PakimonGO Map')),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    return RefreshIndicator(
      onRefresh: _viewModel.fetchMarkers,
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        child: SizedBox(
          height: MediaQuery.of(context).size.height,
          child: _buildContent(),
        ),
      ),
    );
  }

  Widget _buildContent() {
    if (_viewModel.isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_viewModel.error != null) {
      return ErrorRetryView(
        message: _viewModel.error!,
        onRetry: _viewModel.fetchMarkers,
        isOffline: _viewModel.isOffline,
      );
    }

    if (!AppConfig.hasMapboxToken) {
      return _buildNoTokenFallback();
    }

    return Stack(
      children: [
        MapWidget(
          styleUri: MapboxStyles.MAPBOX_STREETS,
          viewport: CameraViewportState(
            center: Point(coordinates: Position(0, 0)),
            zoom: 2.0,
          ),
        ),
        if (_viewModel.hasMarkers) _buildMarkerOverlay(),
      ],
    );
  }

  Widget _buildNoTokenFallback() {
    return const Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.map, size: 64, color: Colors.grey),
          SizedBox(height: 12),
          Text('Map unavailable — set MAPBOX_ACCESS_TOKEN',
              style: TextStyle(color: Colors.grey)),
        ],
      ),
    );
  }

  Widget _buildMarkerOverlay() {
    final clusters = _viewModel.clusters;
    final hasClusters = clusters.isNotEmpty;

    return Positioned(
      left: 12,
      bottom: 12,
      child: GestureDetector(
        onTap: _openMarkerList,
        child: Card(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.location_on, size: 18, color: Colors.green),
                const SizedBox(width: 6),
                hasClusters
                    ? Text(
                        '${clusters.length} clusters · ${_viewModel.markerCount} sightings',
                        style: Theme.of(context).textTheme.bodyMedium)
                    : Text('${_viewModel.markerCount} sightings',
                        style: Theme.of(context).textTheme.bodyMedium),
                const SizedBox(width: 4),
                const Icon(Icons.chevron_right, size: 16),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _openMarkerList() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => MarkerListScreen(markers: _viewModel.markers),
      ),
    );
  }
}
