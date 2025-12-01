# HomeController iOS App

iOS remote control app for home automation via Raspberry Pi backend.

## Setup

### 1. Configure Backend URL

Copy the example secrets file and add your Raspberry Pi IP address:

```bash
cd HomeController/HomeController
cp Secrets.swift.example Secrets.swift
cp Info.plist.example Info.plist
```

Then edit `Secrets.swift` and change the `backendURL` to your Raspberry Pi's IP address:

```swift
static let backendURL = "http://192.168.1.100:8000"
```

Then edit `Info.plist` and replace `YOUR_RASPBERRY_PI_IP` with your actual IP (must match Secrets.swift):

```xml
<key>192.168.1.100</key>  <!-- Replace YOUR_RASPBERRY_PI_IP with your IP -->
```

**Important:** Use the same IP address in both files!

### 2. Build and Run

Open the project in Xcode and build to your device.

**Note:** If Xcode shows an error about Info.plist, configure it in Build Settings:

1. Select your project → HomeController target → Build Settings
2. Search for "Info.plist File"
3. Set to: `HomeController/Info.plist`

## Security

- `Secrets.swift` and `Info.plist` are gitignored and should never be committed
- Use `Secrets.swift.example` and `Info.plist.example` as templates for other developers
- Each developer should create their own configuration files with their Raspberry Pi IP address

## Features

- **AC Control**: Turn on/off aircon and heater, adjust temperature, set timers
- **Light Control**: Control brightness modes and turn lights on/off
- **Settings**: View current configuration
