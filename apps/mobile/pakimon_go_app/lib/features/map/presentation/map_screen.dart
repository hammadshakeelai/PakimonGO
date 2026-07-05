import 'package:flutter/material.dart' hide Visibility;
import 'package:mapbox_maps_flutter/mapbox_maps_flutter.dart';

import '../../../core/config/app_config.dart';
import '../../../shared/models/submission_marker.dart';
import '../../../shared/widgets/error_retry_view.dart';
import '../../capture/data/capture_repository.dart';
import '../../species/presentation/species_detail_screen.dart';
import '../domain/map_viewmodel.dart';
import 'marker_list_screen.dart';

class MapScreen extends StatefulWidget {
  final MapViewModel? viewModel;

  /// Called when the user taps the capture button on the map — the
  /// home shell switches to the Capture tab.
  final VoidCallback? onCameraTap;

  const MapScreen({super.key, this.viewModel, this.onCameraTap});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  late final MapViewModel _viewModel;
  // Only dispose a viewmodel this screen created itself — an injected one
  // belongs to the caller (HomeScreen keeps it across tab switches).
  late final bool _ownsViewModel;
  MapboxMap? _map;
  CircleAnnotationManager? _circles;
  final Map<String, SubmissionMarker> _annotationToMarker = {};

  @override
  void initState() {
    super.initState();
    _ownsViewModel = widget.viewModel == null;
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
    if (_ownsViewModel) _viewModel.dispose();
    super.dispose();
  }

  void _onViewModelChanged() {
    if (!mounted) return;
    setState(() {});
    _drawMarkers();
  }

  // ---- Mapbox wiring -------------------------------------------------

  Future<void> _onMapCreated(MapboxMap map) async {
    _map = map;
    _circles = await map.annotations.createCircleAnnotationManager();
    _circles!.tapEvents(onTap: (annotation) {
      final marker = _annotationToMarker[annotation.id];
      if (marker != null) _openMarker(marker);
    });
    await _drawMarkers();
  }

  Future<void> _drawMarkers() async {
    final circles = _circles;
    if (circles == null) return;
    final markers =
        _viewModel.markers.where((m) => m.hasValidLocation).toList();
    await circles.deleteAll();
    _annotationToMarker.clear();
    if (markers.isEmpty) return;

    for (final marker in markers) {
      final annotation = await circles.create(CircleAnnotationOptions(
        geometry: Point(
          coordinates: Position(marker.longitude, marker.latitude),
        ),
        circleRadius: 10,
        circleColor: _statusColor(marker.status).toARGB32(),
        circleStrokeWidth: 2.5,
        circleStrokeColor: 0xFFFFFFFF,
        circleOpacity: 0.9,
      ));
      _annotationToMarker[annotation.id] = marker;
    }
    await _fitCameraTo(markers);
  }

  Color _statusColor(String status) => switch (status) {
        'scored' => Colors.green,
        'ai_evaluated' => Colors.orange,
        'capped' => Colors.blue,
        _ => Colors.grey,
      };

  Future<void> _fitCameraTo(List<SubmissionMarker> markers) async {
    final map = _map;
    if (map == null || markers.isEmpty) return;
    var minLat = markers.first.latitude, maxLat = markers.first.latitude;
    var minLng = markers.first.longitude, maxLng = markers.first.longitude;
    for (final m in markers) {
      if (m.latitude < minLat) minLat = m.latitude;
      if (m.latitude > maxLat) maxLat = m.latitude;
      if (m.longitude < minLng) minLng = m.longitude;
      if (m.longitude > maxLng) maxLng = m.longitude;
    }
    final spread =
        (maxLat - minLat).abs() + (maxLng - minLng).abs(); // rough degrees
    final zoom = spread < 0.2
        ? 11.0
        : spread < 1
            ? 8.5
            : spread < 5
                ? 6.0
                : spread < 20
                    ? 4.0
                    : 2.5;
    await map.setCamera(CameraOptions(
      center: Point(
        coordinates: Position((minLng + maxLng) / 2, (minLat + maxLat) / 2),
      ),
      zoom: zoom,
    ));
  }

  void _openMarker(SubmissionMarker marker) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => SpeciesDetailScreen(marker: marker)),
    );
  }

  // ---- UI ------------------------------------------------------------

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('PakimonGO Map'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Refresh sightings',
            onPressed: _viewModel.fetchMarkers,
          ),
        ],
      ),
      body: _buildBody(),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: widget.onCameraTap == null
          ? null
          : FloatingActionButton.large(
              tooltip: 'Capture wildlife',
              onPressed: widget.onCameraTap,
              child: const Icon(Icons.photo_camera, size: 36),
            ),
    );
  }

  Widget _buildBody() {
    if (_viewModel.isLoading && _viewModel.markers.isEmpty) {
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
          onMapCreated: _onMapCreated,
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
    final theme = Theme.of(context);
    return Positioned(
      left: 12,
      top: 12,
      child: Card(
        child: InkWell(
          borderRadius: BorderRadius.circular(12),
          onTap: _openMarkerList,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.location_on,
                    size: 18, color: theme.colorScheme.primary),
                const SizedBox(width: 6),
                Text('${_viewModel.markerCount} sightings',
                    style: theme.textTheme.bodyMedium),
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

