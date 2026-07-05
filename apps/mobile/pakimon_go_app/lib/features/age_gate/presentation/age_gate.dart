import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../domain/age_gate_service.dart';

/// Wraps the app: shows the neutral age screen until the user is verified,
/// a blocked screen if under 13, and otherwise renders [child].
class AgeGate extends StatefulWidget {
  final AgeGateService service;
  final Widget child;

  const AgeGate({super.key, required this.service, required this.child});

  @override
  State<AgeGate> createState() => _AgeGateState();
}

class _AgeGateState extends State<AgeGate> {
  AgeGateStatus _status = AgeGateStatus.unknown;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    widget.service.load().then((outcome) {
      if (mounted) {
        setState(() {
          _status = outcome.status;
          _loading = false;
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    if (_status == AgeGateStatus.verified) return widget.child;
    if (_status == AgeGateStatus.blocked) return const AgeBlockedScreen();
    return AgeGateInputScreen(
      service: widget.service,
      onVerified: () => setState(() => _status = AgeGateStatus.verified),
      onBlocked: () => setState(() => _status = AgeGateStatus.blocked),
    );
  }
}

class AgeGateInputScreen extends StatefulWidget {
  final AgeGateService service;
  final VoidCallback onVerified;
  final VoidCallback onBlocked;

  const AgeGateInputScreen({
    super.key,
    required this.service,
    required this.onVerified,
    required this.onBlocked,
  });

  @override
  State<AgeGateInputScreen> createState() => _AgeGateInputScreenState();
}

class _AgeGateInputScreenState extends State<AgeGateInputScreen> {
  final _controller = TextEditingController();
  String? _error;
  bool _submitting = false;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    final now = DateTime.now().year;
    final year = int.tryParse(_controller.text.trim());
    if (year == null || year < 1900 || year > now) {
      setState(() => _error = 'Please enter a valid year.');
      return;
    }
    setState(() {
      _submitting = true;
      _error = null;
    });
    final outcome = await widget.service.submitBirthYear(year);
    if (!mounted) return;
    setState(() => _submitting = false);
    if (outcome.status == AgeGateStatus.blocked) {
      widget.onBlocked();
    } else {
      widget.onVerified();
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Icon(Icons.cake_outlined, size: 64, color: Colors.green),
              const SizedBox(height: 16),
              Text(
                'What year were you born?',
                style: theme.textTheme.headlineSmall,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 8),
              Text(
                'We ask this to keep PakimonGO safe and age-appropriate.',
                style: theme.textTheme.bodyMedium,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 32),
              TextField(
                controller: _controller,
                keyboardType: TextInputType.number,
                inputFormatters: [
                  FilteringTextInputFormatter.digitsOnly,
                  LengthLimitingTextInputFormatter(4),
                ],
                textAlign: TextAlign.center,
                decoration: const InputDecoration(
                  labelText: 'Birth year',
                  hintText: 'e.g. 2005',
                  border: OutlineInputBorder(),
                ),
                onSubmitted: (_) => _submit(),
              ),
              if (_error != null) ...[
                const SizedBox(height: 8),
                Text(
                  _error!,
                  style: TextStyle(color: theme.colorScheme.error),
                  textAlign: TextAlign.center,
                ),
              ],
              const SizedBox(height: 24),
              FilledButton(
                onPressed: _submitting ? null : _submit,
                child: Text(_submitting ? 'Please wait…' : 'Continue'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class AgeBlockedScreen extends StatelessWidget {
  const AgeBlockedScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.lock_outline, size: 64, color: Colors.grey),
                const SizedBox(height: 16),
                Text(
                  'Thanks for your interest',
                  style: theme.textTheme.titleLarge,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  "Unfortunately you're not eligible to use PakimonGO right now.",
                  style: theme.textTheme.bodyMedium,
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
