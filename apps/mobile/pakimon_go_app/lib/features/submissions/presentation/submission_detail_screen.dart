import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:pakimon_go_app/core/network/api_config.dart';
import 'package:pakimon_go_app/features/species/presentation/species_detail_screen.dart';
import 'package:pakimon_go_app/shared/models/api_models.dart';
import 'package:pakimon_go_app/shared/models/submission_marker.dart';

class SubmissionDetailScreen extends StatefulWidget {
  final SubmissionResponse submission;

  const SubmissionDetailScreen({super.key, required this.submission});

  @override
  State<SubmissionDetailScreen> createState() => _SubmissionDetailScreenState();
}

class _SubmissionDetailScreenState extends State<SubmissionDetailScreen> {
  @override
  Widget build(BuildContext context) {
    final s = widget.submission;
    final theme = Theme.of(context);
    final ss = s.scoreState;

    final statusColor = switch (ss.status) {
      'scored' => Colors.green,
      'ai_evaluated' => Colors.orange,
      'capped' => Colors.blue,
      _ => Colors.grey,
    };

    return Scaffold(
      appBar: AppBar(
        title: Text(s.realName ?? 'Submission Detail'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildPhoto(theme),
          const SizedBox(height: 16),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.circle, color: statusColor, size: 12),
                      const SizedBox(width: 8),
                      Text(ss.status, style: TextStyle(color: statusColor, fontWeight: FontWeight.bold)),
                      const Spacer(),
                      Text('${ss.visiblePoints ?? 0} pts',
                          style: theme.textTheme.titleLarge?.copyWith(
                            fontWeight: FontWeight.bold,
                            color: theme.colorScheme.primary,
                          )),
                    ],
                  ),
                  const SizedBox(height: 12),
                  _infoRow(theme, 'Species', s.realName ?? 'Unknown'),
                  if (s.animalContext != null)
                    _infoRow(theme, 'Context', s.animalContext!),
                  _infoRow(theme, 'Status', ss.status),
                  _infoRow(theme, 'Submission ID', s.submissionId),
                  _infoRow(theme, 'Media ID', s.mediaAssetId),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          if (ss.explanationSummary != null)
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Score Explanation',
                        style: theme.textTheme.titleMedium),
                    const SizedBox(height: 8),
                    Text(ss.explanationSummary!,
                        style: theme.textTheme.bodyMedium),
                  ],
                ),
              ),
            ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Location', style: theme.textTheme.titleMedium),
                  const SizedBox(height: 8),
                  _infoRow(theme, 'Latitude',
                      '${s.publicLocation['cellLatitude'] ?? 'N/A'}'),
                  _infoRow(theme, 'Longitude',
                      '${s.publicLocation['cellLongitude'] ?? 'N/A'}'),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          OutlinedButton.icon(
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => SpeciesDetailScreen(
                  marker: SubmissionMarker(
                    submissionId: s.submissionId,
                    mediaAssetId: s.mediaAssetId,
                    species: s.realName ?? 'Unknown',
                    status: ss.status,
                    points: ss.visiblePoints ?? 0,
                    latitude: (s.publicLocation['cellLatitude'] as num?)?.toDouble() ?? 0.0,
                    longitude: (s.publicLocation['cellLongitude'] as num?)?.toDouble() ?? 0.0,
                  ),
                ),
              ),
            ),
            icon: const Icon(Icons.info_outline),
            label: const Text('View Species Details'),
          ),
          const SizedBox(height: 32),
        ],
      ),
    );
  }

  Widget _buildPhoto(ThemeData theme) {
    final url = '${ApiConfig.apiBase}/v1/media/files/thumbs/${widget.submission.mediaAssetId}.jpg';
    return ClipRRect(
      borderRadius: BorderRadius.circular(12),
      child: Image.network(
        url,
        height: 250,
        width: double.infinity,
        fit: BoxFit.cover,
        loadingBuilder: (_, child, progress) {
          if (progress == null) return child;
          return Container(
            height: 250,
            color: theme.colorScheme.surfaceContainerHighest,
            child: const Center(child: CircularProgressIndicator()),
          );
        },
        errorBuilder: (_, __, ___) => Container(
          height: 250,
          color: theme.colorScheme.surfaceContainerHighest,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.broken_image, size: 48, color: theme.colorScheme.outline),
              const SizedBox(height: 8),
              Text('Failed to load photo', style: theme.textTheme.bodySmall),
            ],
          ),
        ),
      ),
    );
  }

  Widget _infoRow(ThemeData theme, String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 120,
            child: Text(label,
                style: theme.textTheme.bodySmall
                    ?.copyWith(fontWeight: FontWeight.bold)),
          ),
          Expanded(child: Text(value, style: theme.textTheme.bodyMedium)),
        ],
      ),
    );
  }
}
