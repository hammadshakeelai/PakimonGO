import 'package:flutter/material.dart';

import '../domain/onboarding_service.dart';

/// Shows the onboarding flow once, then renders [child] on every launch after.
class OnboardingGate extends StatefulWidget {
  final OnboardingService service;
  final Widget child;

  const OnboardingGate({super.key, required this.service, required this.child});

  @override
  State<OnboardingGate> createState() => _OnboardingGateState();
}

class _OnboardingGateState extends State<OnboardingGate> {
  bool _loading = true;
  bool _done = false;

  @override
  void initState() {
    super.initState();
    widget.service.isComplete().then((seen) {
      if (mounted) {
        setState(() {
          _done = seen;
          _loading = false;
        });
      }
    });
  }

  Future<void> _finish() async {
    await widget.service.complete();
    if (mounted) setState(() => _done = true);
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    if (_done) return widget.child;
    return OnboardingScreen(onComplete: _finish);
  }
}

class _OnboardingPageData {
  final IconData icon;
  final String title;
  final String body;
  const _OnboardingPageData(this.icon, this.title, this.body);
}

const _pages = <_OnboardingPageData>[
  _OnboardingPageData(
    Icons.pets,
    'Welcome to PakimonGO',
    'Photograph real animals in the wild, build your species collection, '
        'and explore what others have spotted near you.',
  ),
  _OnboardingPageData(
    Icons.volunteer_activism_outlined,
    'Respect wildlife',
    'Never chase, touch, feed, or corner an animal for a photo. Observe from '
        'a safe distance — points reward calm, respectful sightings, not risky '
        'ones.',
  ),
  _OnboardingPageData(
    Icons.lock_outline,
    'Your location stays private',
    'Public sightings only ever show a rough area, never your exact spot, and '
        'sensitive species are hidden further. Your original photos stay yours. '
        "We only ask for camera and location when you actually use them.",
  ),
  _OnboardingPageData(
    Icons.emoji_events_outlined,
    'How scoring works',
    'Wild animals earn the most. Zoo and pet photos are capped, and duplicates '
        "don't score. An AI reviews each photo — it isn't perfect, so scores can "
        'change after review.',
  ),
];

class OnboardingScreen extends StatefulWidget {
  final VoidCallback onComplete;

  const OnboardingScreen({super.key, required this.onComplete});

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  final _controller = PageController();
  int _page = 0;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  bool get _isLast => _page == _pages.length - 1;

  void _next() {
    if (_isLast) {
      widget.onComplete();
    } else {
      _controller.nextPage(
        duration: const Duration(milliseconds: 250),
        curve: Curves.easeInOut,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            Align(
              alignment: Alignment.centerRight,
              child: TextButton(
                onPressed: widget.onComplete,
                child: const Text('Skip'),
              ),
            ),
            Expanded(
              child: PageView.builder(
                controller: _controller,
                itemCount: _pages.length,
                onPageChanged: (i) => setState(() => _page = i),
                itemBuilder: (context, i) {
                  final page = _pages[i];
                  return Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 32),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(page.icon, size: 96, color: Colors.green),
                        const SizedBox(height: 32),
                        Text(
                          page.title,
                          style: theme.textTheme.headlineSmall,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 16),
                        Text(
                          page.body,
                          style: theme.textTheme.bodyLarge,
                          textAlign: TextAlign.center,
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(_pages.length, (i) {
                final active = i == _page;
                return AnimatedContainer(
                  duration: const Duration(milliseconds: 200),
                  margin: const EdgeInsets.symmetric(horizontal: 4),
                  width: active ? 20 : 8,
                  height: 8,
                  decoration: BoxDecoration(
                    color: active
                        ? theme.colorScheme.primary
                        : theme.colorScheme.outlineVariant,
                    borderRadius: BorderRadius.circular(4),
                  ),
                );
              }),
            ),
            Padding(
              padding: const EdgeInsets.all(24),
              child: SizedBox(
                width: double.infinity,
                child: FilledButton(
                  onPressed: _next,
                  child: Text(_isLast ? 'Get started' : 'Next'),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
