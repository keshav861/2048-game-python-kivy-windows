[app]
title = 2048 Game
package.name = game2048
package.domain = org.game2048
source.dir = .
source.include_exts = py,png,jpg,otf,ttf,json
source.include_patterns = ../assets/*,../*.json
version = 1.0

# Requirements - minimal dependencies
requirements = python3,kivy==2.2.1,pillow,sdl2_ttf==2.0.15

# Android specific
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.arch = arm64-v8a
android.presplash.filename = %(source.dir)s/../assets/icon/icon-512.png
android.icon.filename = %(source.dir)s/../assets/icon/icon-512.png
android.presplash_color = #FFFFFF
android.release_artifact = apk

# Optimization settings
android.enable_androidx = True
android.enable_suspended_screen = False
android.enable_screen_wake = False
android.wakelock = False
android.meta_data = android.max_aspect=2.1
android.allow_backup = False

# Build optimization
android.strip = true
android.optimize_python = true
android.extra_manifest_application_arguments = android:extractNativeLibs="true"
android.meta_data = android:installLocation="auto"

# Include only necessary files
android.add_src = ../assets/fonts:fonts ../assets/icon:icon
android.whitelist = lib-dynload/_csv.so

# Remove unused features
android.enable_new_layout = False
android.copy_libs = False

[buildozer]
log_level = 2
warn_on_root = 1
