import 'package:flutter/material.dart';
import 'package:pakimon_go_app/core/auth/auth_service.dart';
import 'package:pakimon_go_app/features/profile/domain/profile_viewmodel.dart';

/// "Delete My Account" control: confirm dialog -> DELETE /v1/users/me ->
/// logout on success. Split out of profile_screen.dart to keep that file
/// under the project's 300-line convention.
class DeleteAccountButton extends StatelessWidget {
  final ProfileViewModel viewModel;
  final AuthService authService;

  const DeleteAccountButton({
    super.key,
    required this.viewModel,
    required this.authService,
  });

  Future<void> _confirmAndDelete(BuildContext context) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Delete your account?'),
        content: const Text(
          'This permanently deactivates your account and removes your '
          'personal info (age band, region). Your past captures stay '
          'attributed to a deactivated account. This cannot be undone.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(false),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(true),
            child: Text('Delete',
                style: TextStyle(color: Theme.of(ctx).colorScheme.error)),
          ),
        ],
      ),
    );
    if (confirmed != true || !context.mounted) return;

    final ok = await viewModel.deleteAccount();
    if (!context.mounted) return;
    if (ok) {
      Navigator.of(context).popUntil((r) => r.isFirst);
      authService.logout();
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
              viewModel.deleteError ?? 'Could not delete account. Try again.'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return SizedBox(
      width: double.infinity,
      child: TextButton.icon(
        key: const Key('delete_account_button'),
        onPressed: () => _confirmAndDelete(context),
        icon: Icon(Icons.delete_forever, color: theme.colorScheme.error),
        label: Text('Delete My Account',
            style: TextStyle(color: theme.colorScheme.error)),
      ),
    );
  }
}
