import 'package:flutter/material.dart';
import 'package:mapbox_maps_flutter/mapbox_maps_flutter.dart';

import 'core/config/app_config.dart';
import 'features/capture/presentation/capture_screen.dart';
import 'features/map/presentation/map_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  if (AppConfig.hasMapboxToken) {
    MapboxOptions.setAccessToken(AppConfig.mapboxAccessToken);
  }

  runApp(const PakimonGoApp());
}

class PakimonGoApp extends StatelessWidget {
  const PakimonGoApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PakimonGO',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _currentIndex = 0;

  final _screens = const [
    MapScreen(),
    CaptureScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (i) => setState(() => _currentIndex = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.map), label: 'Map'),
          NavigationDestination(icon: Icon(Icons.camera_alt), label: 'Capture'),
        ],
      ),
    );
  }
}
