# Changelog

All notable changes to ValTimer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2025-10-29

### Added
- **Bilingual Support (Vietnamese/English)** - Full language switching between Vietnamese and English
- **Language Toggle Button** - EN/VI button to switch languages instantly
- **Live Position Updates** - Change countdown overlay position while app is running (no restart needed)
- **Collapsible Info Panels** - Info and About panels expand inline instead of popup windows
- **Mutual Exclusion** - Opening one panel automatically closes the other
- **EXIT Button** - Added EXIT button to main window (in addition to system tray)

### Changed
- **Countdown Display** - Removed "s" suffix (45s → 45)
- **Decimal Display** - Show decimals only when time < 7s (critical period)
- **Time Thresholds** - New color scheme:
  - Cyan (#00d9ff): 45s-21s (safe period)
  - Yellow (#ffeb3b): 20s-11s (warning)
  - Orange (#ffa502): 10s-8s (danger)
  - Red (#ff4655): <7s with decimals (critical)
- **Multi-Resolution Corners** - All 4 corners supported for 1080p, 2K, and 4:3
- **Window Size** - Increased to 600x600 to accommodate new buttons
- **Button Styling** - Improved 3-button layout (Spike Info, About Me, EN/VI):
  - Spike Info & About Me: Blue (#3a5f8f), width=16, height=2
  - EN/VI: Green (#5f8f3a), width=10, height=2
  - Centered layout with better spacing
- **Font Sizes** - Optimized at 10pt bold for all info buttons
- **Info Panel Display** - Panels appear ABOVE buttons instead of below
- **Windowed Fullscreen Warning** - Orange warning text replaces auto-detect subtitle
- **Stop Button Width** - Increased to 18 to fit Vietnamese text "DỪNG BỘ ĐẾM"

### Fixed
- **Vietnamese Text Overflow** - Increased button widths to prevent text cutoff
- **Button Alignment** - Centered 3-button layout for better aesthetics
- **Panel Toggle** - Fixed toggle button text updates when switching languages

### Removed
- **All Tooltips** - Removed hover tooltips from all buttons for cleaner UX
- **Features Line** - Removed from About panel for concise information
- **"About" Button Name** - Changed to "About Me" for personalization

### Language Support Details
- **Vietnamese UI**:
  - Title: "ValTimer - Valorant Spike Timer" (kept in English)
  - Resolution: "Độ Phân Giải"
  - Position: "Vị Trí Overlay"
  - Buttons: "THOÁT", "DỪNG BỘ ĐẾM"
  - Info: "Thông Tin Spike", "Về Tác Giả"
  - Spike mechanics and warnings fully translated
  
- **English UI**:
  - All original English text maintained
  - Consistent styling across languages

## [1.2.0] - 2025-10-27

### Added
- **Custom Resolution ROI Finder** - New `find_spike_position.py` tool to find Spike position for any resolution
- **System Tray Integration** - Minimize to system tray with Show/Exit menu
- **Spike Info Button** - In-app popup with detailed Spike mechanics and timings
- **Valorant-Themed UI** - Modern card-style interface with Valorant colors (#0f1923, #ff4655)
- **Multi-Resolution Support** - Added 4:3 (1440x1080) resolution support
- **Debug Mode** - Hidden debug mode for ROI visualization (toggle with DEBUG_MODE flag)
- **Icon Customization** - `app_icon.py` tool with 4 different icon styles
- **Tooltips** - Helpful tooltips on all buttons for better UX
- **Keyboard Shortcuts** - ESC key to stop detection or close app
- **MIT License** - Open source under MIT License
- **Requirements.txt** - Dependency management file

### Changed
- **UI Redesign** - Increased window size to 600x430 for better spacing
- **Panel Styling** - Card-style panels with borders and improved padding
- **Button Layout** - Better organized resolution buttons with consistent width
- **Title Font** - Increased to 20pt bold with ⚡ icon
- **Info Button** - Shortened to "ℹ️ Info" (width: 10) for compact design
- **Spike Info Popup** - Optimized size to 420x365 with accurate Valorant mechanics
- **README.md** - Comprehensive documentation with custom resolution guide

### Fixed
- **4:3 Resolution Detection** - Fixed ROI coordinates for 1440x1080 resolution
- **Debug Window Positioning** - Fixed off-screen issues on 4:3 displays
- **Template Matching** - Improved edge detection with Canny thresholds (100, 200)
- **Cooldown Period** - Increased to 50 seconds to prevent duplicate detections

### Removed
- **Old ROI Finder** - Replaced `roi_finder.py` with better `find_spike_position.py`
- **Donate Button** - Removed per user request
- **Audio Range Info** - Removed 60m audio information from Spike Info
- **Scrollbar** - Removed from Spike Info popup for cleaner look

## [1.0.0] - 2025-10-XX

### Added
- **Initial Release** - First version of ValTimer
- **Spike Detection** - OpenCV template matching with Canny edge detection
- **Countdown Timer** - 45-second overlay countdown
- **Resolution Support** - 1920x1080 and 2560x1440 configurations
- **Basic UI** - Simple tkinter interface
- **PyInstaller Build** - Windows executable generation

### Technical Details
- Detection threshold: 0.15
- Scan interval: 0.05 seconds
- Countdown duration: 45 seconds
- Cooldown period: 50 seconds

---

## Version History

### v1.2.0 (Current)
- Major UI overhaul
- System tray support
- Custom resolution tool
- Enhanced documentation

### v1.0.0 (Initial)
- Basic spike detection
- Simple countdown
- 2 resolutions

---

## Upcoming Features (Roadmap)

### Planned for v1.3.0
- [ ] Multiple language support
- [ ] Sound notifications
- [ ] Custom countdown duration
- [ ] Statistics tracking
- [ ] Auto-update feature

### Planned for v2.0.0
- [ ] Agent ability timers
- [ ] Ultimate tracking
- [ ] Match history
- [ ] Cloud sync settings

---

## Links

- **Repository**: https://github.com/trtrantnt/ValTimerv1.2
- **Issues**: https://github.com/trtrantnt/ValTimerv1.2/issues
- **Releases**: https://github.com/trtrantnt/ValTimerv1.2/releases

---

## Contributors

Special thanks to all contributors who helped make ValTimer better!

- Initial development and design
- UI/UX improvements
- Bug fixes and testing
- Documentation

---

*For more details on each release, visit the [Releases](https://github.com/trtrantnt/ValTimerv1.2/releases) page.*
