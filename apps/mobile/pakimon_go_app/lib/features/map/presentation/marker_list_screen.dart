import 'package:flutter/material.dart';
import 'package:pakimon_go_app/shared/models/submission_marker.dart';
import 'package:pakimon_go_app/features/species/presentation/species_detail_screen.dart';

class MarkerListScreen extends StatelessWidget {
  final List<SubmissionMarker> markers;

  const MarkerListScreen({super.key, required this.markers});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Sightings')),
      body: markers.isEmpty
          ? const Center(child: Text('No sightings yet'))
          : ListView.separated(
              itemCount: markers.length,
              separatorBuilder: (_, __) => const Divider(height: 1),
              itemBuilder: (context, index) {
                final marker = markers[index];
                return ListTile(
                  leading: CircleAvatar(
                    backgroundColor: _statusColor(marker.status),
                    child: Text('${marker.points}',
                        style: const TextStyle(
                            color: Colors.white, fontSize: 12)),
                  ),
                  title: Text(marker.species),
                  subtitle: Text(
                    '${marker.status} · ${marker.latitude.toStringAsFixed(3)}, ${marker.longitude.toStringAsFixed(3)}',
                    style: const TextStyle(fontSize: 12),
                  ),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () => Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) =>
                          SpeciesDetailScreen(marker: marker),
                    ),
                  ),
                );
              },
            ),
    );
  }

  Color _statusColor(String status) {
    switch (status) {
      case 'scored':
        return Colors.green;
      case 'ai_evaluated':
        return Colors.orange;
      case 'capped':
        return Colors.blue;
      case 'pending':
        return Colors.grey;
      default:
        return Colors.grey;
    }
  }
}
