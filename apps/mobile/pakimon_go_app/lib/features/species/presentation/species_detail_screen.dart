import 'package:flutter/material.dart';
import 'package:pakimon_go_app/core/network/api_config.dart';
import 'package:pakimon_go_app/shared/models/submission_marker.dart';

class SpeciesDetailScreen extends StatelessWidget {
  final SubmissionMarker marker;

  const SpeciesDetailScreen({super.key, required this.marker});

  // The derivative pipeline writes .webp thumbnails.
  String get _thumbnailUrl =>
      '${ApiConfig.baseUrl}/v1/media/files/thumbs/${marker.mediaAssetId}.webp';

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(marker.species)),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildPhoto(theme),
            const SizedBox(height: 16),
            _buildInfoCard(theme),
          ],
        ),
      ),
    );
  }

  Widget _buildPhoto(ThemeData theme) {
    if (marker.mediaAssetId.isEmpty) {
      return _buildPhotoPlaceholder(theme, 'Photo not available');
    }
    return ClipRRect(
      borderRadius: BorderRadius.circular(12),
      child: Image.network(
        _thumbnailUrl,
        width: double.infinity,
        height: 200,
        fit: BoxFit.cover,
        errorBuilder: (context, error, stackTrace) =>
            _buildPhotoPlaceholder(theme, 'Failed to load photo'),
        loadingBuilder: (context, child, loadingProgress) {
          if (loadingProgress == null) return child;
          return _buildPhotoPlaceholder(theme, 'Loading photo…');
        },
      ),
    );
  }

  Widget _buildPhotoPlaceholder(ThemeData theme, String message) {
    return Container(
      width: double.infinity,
      height: 200,
      decoration: BoxDecoration(
        color: theme.colorScheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.image, size: 48, color: Colors.grey),
            const SizedBox(height: 8),
            Text(message, style: const TextStyle(color: Colors.grey)),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoCard(ThemeData theme) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.biotech, size: 20),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(marker.species,
                      style: theme.textTheme.titleMedium),
                ),
              ],
            ),
            const Divider(),
            _buildInfoRow(Icons.score, 'Points', '${marker.points}'),
            const SizedBox(height: 8),
            _buildInfoRow(Icons.check_circle, 'Status', marker.status),
            const SizedBox(height: 8),
            _buildInfoRow(Icons.location_on, 'Latitude',
                marker.latitude.toStringAsFixed(4)),
            const SizedBox(height: 8),
            _buildInfoRow(Icons.location_on, 'Longitude',
                marker.longitude.toStringAsFixed(4)),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow(IconData icon, String label, String value) {
    return Row(
      children: [
        Icon(icon, size: 16, color: Colors.grey),
        const SizedBox(width: 8),
        Text('$label: ', style: const TextStyle(color: Colors.grey)),
        Expanded(child: Text(value)),
      ],
    );
  }
}
