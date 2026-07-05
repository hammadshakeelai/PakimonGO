import 'package:flutter/material.dart';
import 'package:pakimon_go_app/features/collection/domain/collection_viewmodel.dart';
import 'package:pakimon_go_app/features/species/presentation/species_detail_screen.dart';
import 'package:pakimon_go_app/shared/models/submission_marker.dart';
import 'package:pakimon_go_app/shared/widgets/error_retry_view.dart';

class CollectionScreen extends StatefulWidget {
  final CollectionViewModel viewModel;

  const CollectionScreen({super.key, required this.viewModel});

  @override
  State<CollectionScreen> createState() => _CollectionScreenState();
}

class _CollectionScreenState extends State<CollectionScreen> {
  @override
  void initState() {
    super.initState();
    widget.viewModel.addListener(_onChanged);
    widget.viewModel.fetchCollection();
  }

  @override
  void dispose() {
    widget.viewModel.removeListener(_onChanged);
    super.dispose();
  }

  void _onChanged() => setState(() {});

  static const _sortOptions = [
    ('totalPoints', 'Points'),
    ('species', 'Species'),
    ('captureCount', 'Count'),
    ('lastCaptured', 'Recent'),
  ];

  static const _contextOptions = [
    (null, 'All'),
    ('wild', 'Wild'),
    ('zoo', 'Zoo'),
    ('pet', 'Pet'),
  ];

  @override
  Widget build(BuildContext context) {
    final vm = widget.viewModel;
    final theme = Theme.of(context);

    if (vm.state == CollectionLoadState.loading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (vm.state == CollectionLoadState.error) {
      return ErrorRetryView(
        message: vm.error ?? 'Something went wrong.',
        onRetry: vm.refresh,
        isOffline: vm.isOffline,
      );
    }

    if (vm.state == CollectionLoadState.empty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.collections_bookmark,
                size: 64, color: theme.colorScheme.outline),
            const SizedBox(height: 16),
            Text('No species collected yet',
                style: theme.textTheme.titleMedium),
            const SizedBox(height: 8),
            Text('Go capture some wildlife!',
                style: theme.textTheme.bodyMedium),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: () async => vm.refresh(),
      child: ListView.builder(
        itemCount: vm.entries.length + 2,
        itemBuilder: (_, i) {
          if (i == 0) {
            return Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Row(
                children: [
                  Expanded(
                    child: DropdownButtonFormField<String>(
                      initialValue: vm.sortBy,
                      decoration: const InputDecoration(
                        labelText: 'Sort',
                        border: OutlineInputBorder(),
                        isDense: true,
                      ),
                      items: _sortOptions
                          .map((o) => DropdownMenuItem(
                                value: o.$1,
                                child: Text(o.$2),
                              ))
                          .toList(),
                      onChanged: (v) {
                        if (v != null) vm.setSortBy(v);
                      },
                    ),
                  ),
                  const SizedBox(width: 12),
                  IconButton(
                    icon: Icon(vm.sortOrder == 'desc'
                        ? Icons.arrow_downward
                        : Icons.arrow_upward),
                    onPressed: () => vm.setSortOrder(
                        vm.sortOrder == 'desc' ? 'asc' : 'desc'),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: DropdownButtonFormField<String?>(
                      initialValue: vm.contextFilter,
                      decoration: const InputDecoration(
                        labelText: 'Context',
                        border: OutlineInputBorder(),
                        isDense: true,
                      ),
                      items: _contextOptions
                          .map((o) => DropdownMenuItem(
                                value: o.$1,
                                child: Text(o.$2),
                              ))
                          .toList(),
                      onChanged: (v) => vm.setContextFilter(v),
                    ),
                  ),
                ],
              ),
            );
          }
          if (i == 1) {
            return Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Text('${vm.total} species',
                  style: theme.textTheme.bodySmall),
            );
          }
          final e = vm.entries[i - 2];
          return ListTile(
            leading: CircleAvatar(
              backgroundColor: theme.colorScheme.primaryContainer,
              child: Text(
                e.species.isNotEmpty
                    ? e.species[0].toUpperCase()
                    : '?',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  color: theme.colorScheme.onPrimaryContainer,
                ),
              ),
            ),
            title: Text(e.species),
            subtitle: Text(
              '${e.captureCount}x · ${e.totalPoints} pts${e.context != null ? ' · ${e.context![0].toUpperCase()}${e.context!.substring(1)}' : ''}',
            ),
            trailing: Text(
              '${e.totalPoints}',
              style: theme.textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.bold,
                color: theme.colorScheme.primary,
              ),
            ),
            onTap: () => Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => SpeciesDetailScreen(
                  marker: SubmissionMarker(
                    submissionId: '',
                    mediaAssetId: '',
                    species: e.species,
                    status: 'scored',
                    points: e.totalPoints,
                    latitude: 0,
                    longitude: 0,
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
