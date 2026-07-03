# PakimonGO ProGuard/R8 keep rules
# R8 (isMinifyEnabled) strips unused Java/Kotlin classes in release builds.
# Plugins with reflection / JNI need explicit keep rules or they crash at runtime.

# Flutter embedding + plugins
-keep class io.flutter.** { *; }
-keep class io.flutter.plugins.** { *; }
-keep class io.flutter.embedding.** { *; }
-dontwarn io.flutter.**

# Mapbox Maps SDK (native bindings + Flutter plugin)
-keep class com.mapbox.** { *; }
-keep interface com.mapbox.** { *; }
-dontwarn com.mapbox.**

# Google Play services / Google Sign-In
-keep class com.google.android.gms.** { *; }
-dontwarn com.google.android.gms.**

# Kotlin runtime metadata used by plugins
-dontwarn kotlin.**
-dontwarn kotlinx.**
