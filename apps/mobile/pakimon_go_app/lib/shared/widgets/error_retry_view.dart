import 'package:flutter/material.dart';

/// A consistent full-screen error state with a Retry action. Distinguishes a
/// transport/offline failure (cloud-off) from a server-side error.
class ErrorRetryView extends StatelessWidget {
  final String message;
  final VoidCallback onRetry;
  final bool isOffline;

  const ErrorRetryView({
    super.key,
    required this.message,
    required this.onRetry,
    this.isOffline = false,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              isOffline ? Icons.cloud_off : Icons.error_outline,
              size: 48,
              color: isOffline ? Colors.grey : Colors.red.shade300,
            ),
            const SizedBox(height: 12),
            Text(
              isOffline ? 'You appear to be offline' : 'Something went wrong',
              style: theme.textTheme.titleMedium,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 8),
            Text(
              message,
              style: theme.textTheme.bodySmall,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),
            FilledButton.tonalIcon(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh),
              label: const Text('Retry'),
            ),
          ],
        ),
      ),
    );
  }
}
