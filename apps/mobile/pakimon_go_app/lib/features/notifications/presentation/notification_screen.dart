import 'package:flutter/material.dart';
import 'package:pakimon_go_app/features/notifications/domain/notification_viewmodel.dart';
import 'package:pakimon_go_app/features/submissions/presentation/submission_detail_screen.dart';

class NotificationScreen extends StatefulWidget {
  final NotificationViewModel viewModel;

  const NotificationScreen({super.key, required this.viewModel});

  @override
  State<NotificationScreen> createState() => _NotificationScreenState();
}

class _NotificationScreenState extends State<NotificationScreen> {
  @override
  void initState() {
    super.initState();
    widget.viewModel.addListener(_onChanged);
    widget.viewModel.fetchNotifications();
  }

  @override
  void dispose() {
    widget.viewModel.removeListener(_onChanged);
    super.dispose();
  }

  void _onChanged() => setState(() {});

  Future<void> _onRefresh() => widget.viewModel.fetchNotifications();

  @override
  Widget build(BuildContext context) {
    final vm = widget.viewModel;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Notifications'),
      ),
      body: _buildBody(vm),
    );
  }

  Widget _buildBody(NotificationViewModel vm) {
    if (vm.isLoading && vm.notifications.isEmpty) {
      return const Center(child: CircularProgressIndicator());
    }

    if (vm.error != null && vm.notifications.isEmpty) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.error_outline, size: 48, color: Colors.red),
            const SizedBox(height: 16),
            Text('Failed to load notifications',
                style: Theme.of(context).textTheme.bodyLarge),
            const SizedBox(height: 8),
            FilledButton.tonal(
              onPressed: _onRefresh,
              child: const Text('Retry'),
            ),
          ],
        ),
      );
    }

    if (vm.notifications.isEmpty) {
      return const Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.notifications_none, size: 64, color: Colors.grey),
            SizedBox(height: 16),
            Text('No notifications yet'),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _onRefresh,
      child: ListView.builder(
        itemCount: vm.notifications.length,
        itemBuilder: (context, index) {
          final n = vm.notifications[index];
          return Card(
            margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
            color: n.isRead ? null : Theme.of(context).colorScheme.primaryContainer,
            child: ListTile(
              leading: Icon(
                n.isRead ? Icons.notifications : Icons.notifications_active,
                color: n.isRead ? Colors.grey : Theme.of(context).colorScheme.primary,
              ),
              title: Text(
                n.title,
                style: TextStyle(
                  fontWeight: n.isRead ? FontWeight.normal : FontWeight.bold,
                ),
              ),
              subtitle: n.body != null ? Text(n.body!) : null,
              onTap: () async {
                await widget.viewModel.markAsRead(n);
                if (n.referenceType == 'submission' &&
                    n.referenceId != null) {
                  final sub =
                      await widget.viewModel.getSubmissionById(n.referenceId!);
                  if (sub != null && context.mounted) {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => SubmissionDetailScreen(
                          submission: sub,
                          repository: widget.viewModel.repository,
                        ),
                      ),
                    );
                  }
                }
              },
            ),
          );
        },
      ),
    );
  }
}
