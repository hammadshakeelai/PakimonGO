import 'package:flutter/material.dart';
import 'package:pakimon_go_app/features/leaderboard/domain/leaderboard_viewmodel.dart';
import 'package:pakimon_go_app/shared/widgets/error_retry_view.dart';

class LeaderboardScreen extends StatefulWidget {
  final LeaderboardViewModel viewModel;

  const LeaderboardScreen({super.key, required this.viewModel});

  @override
  State<LeaderboardScreen> createState() => _LeaderboardScreenState();
}

class _LeaderboardScreenState extends State<LeaderboardScreen> {
  @override
  void initState() {
    super.initState();
    widget.viewModel.addListener(_onChanged);
    widget.viewModel.fetchLeaderboard();
  }

  @override
  void dispose() {
    widget.viewModel.removeListener(_onChanged);
    super.dispose();
  }

  void _onChanged() => setState(() {});

  Future<void> _onRefresh() => widget.viewModel.fetchLeaderboard();

  @override
  Widget build(BuildContext context) {
    final vm = widget.viewModel;
    final theme = Theme.of(context);

    if (vm.isLoading && vm.entries.isEmpty) {
      return const Center(child: CircularProgressIndicator());
    }

    if (vm.error != null && vm.entries.isEmpty) {
      return ErrorRetryView(
        message: vm.error!,
        onRetry: _onRefresh,
        isOffline: vm.isOffline,
      );
    }

    if (vm.entries.isEmpty) {
      return const Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.leaderboard, size: 64, color: Colors.grey),
            SizedBox(height: 16),
            Text('No leaderboard data yet'),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _onRefresh,
      child: ListView.builder(
        itemCount: vm.entries.length,
        itemBuilder: (context, index) {
          final entry = vm.entries[index];
          final rank = index + 1;
          return ListTile(
            leading: CircleAvatar(
              backgroundColor: rank <= 3
                  ? theme.colorScheme.primaryContainer
                  : theme.colorScheme.surfaceContainerHighest,
              child: Text('$rank', style: theme.textTheme.bodySmall),
            ),
            title: Text(entry.userId),
            subtitle: Text(
              '${entry.submissionCount} submission${entry.submissionCount == 1 ? '' : 's'}',
            ),
            trailing: Text(
              '${entry.totalScore} pts',
              style: theme.textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.bold,
                color: theme.colorScheme.primary,
              ),
            ),
          );
        },
      ),
    );
  }
}
