import 'package:flutter/material.dart';
import 'package:pakimon_go_app/features/leaderboard/domain/leaderboard_viewmodel.dart';
import 'package:pakimon_go_app/features/moderation/presentation/report_dialog.dart';
import 'package:pakimon_go_app/shared/widgets/error_retry_view.dart';

class LeaderboardScreen extends StatefulWidget {
  final LeaderboardViewModel viewModel;

  /// The signed-in user's id — used to hide report/block on their own row.
  final String? currentUserId;

  const LeaderboardScreen({super.key, required this.viewModel, this.currentUserId});

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
            trailing: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  '${entry.totalScore} pts',
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: theme.colorScheme.primary,
                  ),
                ),
                if (entry.userId != widget.currentUserId)
                  PopupMenuButton<String>(
                    tooltip: 'More',
                    icon: const Icon(Icons.more_vert, size: 20),
                    onSelected: (action) => _onEntryAction(action, entry.userId),
                    itemBuilder: (_) => const [
                      PopupMenuItem(
                        value: 'report',
                        child: ListTile(
                          dense: true,
                          contentPadding: EdgeInsets.zero,
                          leading: Icon(Icons.flag_outlined),
                          title: Text('Report user'),
                        ),
                      ),
                      PopupMenuItem(
                        value: 'block',
                        child: ListTile(
                          dense: true,
                          contentPadding: EdgeInsets.zero,
                          leading: Icon(Icons.block),
                          title: Text('Block user'),
                        ),
                      ),
                    ],
                  ),
              ],
            ),
          );
        },
      ),
    );
  }

  Future<void> _onEntryAction(String action, String userId) async {
    if (action == 'report') {
      await showReportDialog(
        context,
        repository: widget.viewModel.repository,
        targetType: 'user',
        targetId: userId,
        targetLabel: userId,
      );
      return;
    }
    if (action == 'block') {
      final confirmed = await showDialog<bool>(
        context: context,
        builder: (ctx) => AlertDialog(
          title: Text('Block $userId?'),
          content: const Text(
              'Their entries will disappear from your leaderboard. You can '
              'unblock them any time from Profile → Blocked Users.'),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(ctx).pop(false),
              child: const Text('Cancel'),
            ),
            FilledButton(
              onPressed: () => Navigator.of(ctx).pop(true),
              child: const Text('Block'),
            ),
          ],
        ),
      );
      if (confirmed != true || !mounted) return;
      final messenger = ScaffoldMessenger.of(context);
      try {
        await widget.viewModel.repository.blockUser(userId);
        messenger.showSnackBar(SnackBar(content: Text('Blocked $userId.')));
        await widget.viewModel.fetchLeaderboard();
      } catch (_) {
        messenger.showSnackBar(
          const SnackBar(content: Text('Could not block. Please try again.')),
        );
      }
    }
  }
}
