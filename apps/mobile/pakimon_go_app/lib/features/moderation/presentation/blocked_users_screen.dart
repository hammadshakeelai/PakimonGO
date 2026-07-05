import 'package:flutter/material.dart';
import 'package:pakimon_go_app/features/moderation/domain/blocked_users_viewmodel.dart';
import 'package:pakimon_go_app/shared/widgets/error_retry_view.dart';

/// FR-MOD-003: manage the users you have blocked.
class BlockedUsersScreen extends StatefulWidget {
  final BlockedUsersViewModel viewModel;

  const BlockedUsersScreen({super.key, required this.viewModel});

  @override
  State<BlockedUsersScreen> createState() => _BlockedUsersScreenState();
}

class _BlockedUsersScreenState extends State<BlockedUsersScreen> {
  @override
  void initState() {
    super.initState();
    widget.viewModel.addListener(_onChanged);
    widget.viewModel.fetchBlockedUsers();
  }

  @override
  void dispose() {
    widget.viewModel.removeListener(_onChanged);
    super.dispose();
  }

  void _onChanged() => setState(() {});

  Future<void> _unblock(String userId) async {
    final messenger = ScaffoldMessenger.of(context);
    final ok = await widget.viewModel.unblock(userId);
    messenger.showSnackBar(SnackBar(
      content: Text(ok
          ? 'Unblocked $userId. Their content is visible again.'
          : 'Could not unblock. Please try again.'),
    ));
  }

  @override
  Widget build(BuildContext context) {
    final vm = widget.viewModel;
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Blocked Users')),
      body: () {
        if (vm.isLoading && vm.blockedUserIds.isEmpty) {
          return const Center(child: CircularProgressIndicator());
        }
        if (vm.error != null && vm.blockedUserIds.isEmpty) {
          return ErrorRetryView(
            message: vm.error!,
            onRetry: vm.fetchBlockedUsers,
            isOffline: vm.isOffline,
          );
        }
        if (vm.isEmpty) {
          return Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.block, size: 64, color: theme.colorScheme.outline),
                const SizedBox(height: 16),
                Text("You haven't blocked anyone",
                    style: theme.textTheme.titleMedium),
                const SizedBox(height: 8),
                Text(
                  'Blocked users are hidden from your leaderboard.',
                  style: theme.textTheme.bodyMedium,
                ),
              ],
            ),
          );
        }
        return ListView.separated(
          itemCount: vm.blockedUserIds.length,
          separatorBuilder: (_, _) => const Divider(height: 1),
          itemBuilder: (context, index) {
            final userId = vm.blockedUserIds[index];
            return ListTile(
              leading: CircleAvatar(
                backgroundColor: theme.colorScheme.surfaceContainerHighest,
                child: const Icon(Icons.person_off, size: 20),
              ),
              title: Text(userId),
              trailing: TextButton(
                onPressed: () => _unblock(userId),
                child: const Text('Unblock'),
              ),
            );
          },
        );
      }(),
    );
  }
}
