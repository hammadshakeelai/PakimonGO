import 'package:flutter/material.dart';
import 'package:pakimon_go_app/shared/models/submission_marker.dart';

class SpeciesDetailScreen extends StatelessWidget {
  final SubmissionMarker marker;

  const SpeciesDetailScreen({super.key, required this.marker});

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
            _buildPhotoPlaceholder(theme),
            const SizedBox(height: 16),
            _buildInfoCard(theme),
          ],
        ),
      ),
    );
  }

  Widget _buildPhotoPlaceholder(ThemeData theme) {
    return Container(
      width: double.infinity,
      height: 200,
      decoration: BoxDecoration(
        color: theme.colorScheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(12),
      ),
      child: const Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.image, size: 48, color: Colors.grey),
            SizedBox(height: 8),
            Text('Photo preview', style: TextStyle(color: Colors.grey)),
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
