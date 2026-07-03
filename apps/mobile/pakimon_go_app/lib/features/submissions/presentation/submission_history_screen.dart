import 'package:flutter/material.dart';
import 'package:pakimon_go_app/features/submissions/domain/submission_history_viewmodel.dart';
import 'package:pakimon_go_app/features/submissions/presentation/submission_detail_screen.dart';

class SubmissionHistoryScreen extends StatefulWidget {
  final SubmissionHistoryViewModel viewModel;

  const SubmissionHistoryScreen({super.key, required this.viewModel});

  @override
  State<SubmissionHistoryScreen> createState() =>
      _SubmissionHistoryScreenState();
}

class _SubmissionHistoryScreenState extends State<SubmissionHistoryScreen> {
  @override
  void initState() {
    super.initState();
    widget.viewModel.addListener(_onChanged);
    widget.viewModel.fetchSubmissions();
  }

  @override
  void dispose() {
    widget.viewModel.removeListener(_onChanged);
    super.dispose();
  }

  void _onChanged() => setState(() {});

  @override
  Widget build(BuildContext context) {
    if (widget.viewModel.isLoading && widget.viewModel.submissions.isEmpty) {
      return const Center(child: CircularProgressIndicator());
    }

    if (widget.viewModel.error != null && widget.viewModel.submissions.isEmpty) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.error_outline, size: 48, color: Colors.red.shade300),
            const SizedBox(height: 8),
            Text('Failed to load submissions',
                style: Theme.of(context).textTheme.bodyLarge),
            const SizedBox(height: 8),
            FilledButton.tonalIcon(
              onPressed: widget.viewModel.fetchSubmissions,
              icon: const Icon(Icons.refresh),
              label: const Text('Retry'),
            ),
          ],
        ),
      );
    }

    if (widget.viewModel.isEmpty) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.inbox_outlined, size: 64, color: Colors.grey.shade400),
            const SizedBox(height: 8),
            Text('No submissions yet',
                style: Theme.of(context).textTheme.bodyLarge),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: widget.viewModel.fetchSubmissions,
      child: ListView.separated(
        padding: const EdgeInsets.all(8),
        itemCount: widget.viewModel.submissions.length,
        separatorBuilder: (_, __) => const Divider(height: 1),
        itemBuilder: (context, index) {
          final sub = widget.viewModel.submissions[index];
          final statusColor = switch (sub.scoreState.status) {
            'scored' => Colors.green,
            'ai_evaluated' => Colors.orange,
            'capped' => Colors.blue,
            _ => Colors.grey,
          };

          return ListTile(
            leading: CircleAvatar(
              backgroundColor: statusColor.withAlpha(51),
              child: Icon(
                sub.isScored
                    ? Icons.emoji_events
                    : sub.isCapped
                        ? Icons.lock
                        : Icons.hourglass_empty,
                color: statusColor,
                size: 20,
              ),
            ),
            title: Text(sub.realName ?? 'Unknown species',
                maxLines: 1,
                overflow: TextOverflow.ellipsis),
            subtitle: Text(
              '${sub.points} pts  ·  ${sub.scoreState.status}  ·  ${sub.animalContext ?? 'unknown'}',
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            trailing: const Icon(Icons.chevron_right, size: 20),
            onTap: () => Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => SubmissionDetailScreen(submission: sub),
              ),
            ),
          );
        },
      ),
    );
  }
}
