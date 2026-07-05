import 'package:flutter/material.dart';
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';

const _reasons = <(String, String)>[
  ('inappropriate', 'Inappropriate content'),
  ('spam', 'Spam or misleading'),
  ('harassment', 'Harassment or bullying'),
  ('unsafe_animal_interaction', 'Unsafe animal interaction'),
  ('location_abuse', 'Location abuse'),
  ('other', 'Something else'),
];

/// Shows the standard report flow for a submission or a user (FR-MOD-001/002).
/// Reports are confidential; the reported account is not notified.
Future<void> showReportDialog(
  BuildContext context, {
  required CaptureRepository repository,
  required String targetType,
  required String targetId,
  String? targetLabel,
}) async {
  final messenger = ScaffoldMessenger.of(context);
  final submitted = await showDialog<bool>(
    context: context,
    builder: (_) => _ReportDialog(
      repository: repository,
      targetType: targetType,
      targetId: targetId,
      targetLabel: targetLabel,
    ),
  );
  if (submitted == true) {
    messenger.showSnackBar(
      const SnackBar(content: Text('Report submitted. Thank you.')),
    );
  }
}

class _ReportDialog extends StatefulWidget {
  final CaptureRepository repository;
  final String targetType;
  final String targetId;
  final String? targetLabel;

  const _ReportDialog({
    required this.repository,
    required this.targetType,
    required this.targetId,
    this.targetLabel,
  });

  @override
  State<_ReportDialog> createState() => _ReportDialogState();
}

class _ReportDialogState extends State<_ReportDialog> {
  String? _reason;
  final _details = TextEditingController();
  bool _submitting = false;
  String? _error;

  @override
  void dispose() {
    _details.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (_reason == null) return;
    setState(() {
      _submitting = true;
      _error = null;
    });
    try {
      await widget.repository.submitReport(
        targetType: widget.targetType,
        targetId: widget.targetId,
        reason: _reason!,
        details: _details.text.trim(),
      );
      if (mounted) Navigator.of(context).pop(true);
    } on ApiException catch (e) {
      setState(() {
        _submitting = false;
        _error = e.statusCode == 409
            ? 'You have already reported this.'
            : e.message;
      });
    } catch (_) {
      setState(() {
        _submitting = false;
        _error = 'Something went wrong. Please try again.';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final what = widget.targetLabel ??
        (widget.targetType == 'user' ? 'this user' : 'this submission');
    return AlertDialog(
      title: Text('Report $what'),
      content: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            RadioGroup<String>(
              groupValue: _reason,
              onChanged: _submitting
                  ? (_) {}
                  : (v) => setState(() => _reason = v),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  for (final (value, label) in _reasons)
                    RadioListTile<String>(
                      dense: true,
                      contentPadding: EdgeInsets.zero,
                      title: Text(label),
                      value: value,
                    ),
                ],
              ),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: _details,
              enabled: !_submitting,
              maxLength: 500,
              maxLines: 3,
              decoration: const InputDecoration(
                labelText: 'Details (optional)',
                border: OutlineInputBorder(),
              ),
            ),
            if (_error != null)
              Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Text(
                  _error!,
                  style: TextStyle(color: theme.colorScheme.error),
                ),
              ),
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed:
              _submitting ? null : () => Navigator.of(context).pop(false),
          child: const Text('Cancel'),
        ),
        FilledButton(
          onPressed: _reason == null || _submitting ? null : _submit,
          child: _submitting
              ? const SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(strokeWidth: 2),
                )
              : const Text('Report'),
        ),
      ],
    );
  }
}
