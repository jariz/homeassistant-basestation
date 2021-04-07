# Valve Basestation integration for Homeassistant

Read and manage power states for your Valve Index® Base Stations (also referred to as 'Lighthouse V2') through [BLE](https://en.wikipedia.org/wiki/Bluetooth_Low_Energy).

![](https://jari.lol/TYc7q1qt9E.png)  

## Installation

- Ensure [HACS](https://hacs.xyz) is installed.
- Go to Community -> Frontend -> press the three dots (top right corner of screen) -> Custom repositories and add the following information: 
  - Add custom repository URL: https://github.com/jariz/homeassistant-basestation 
  - Category: `Integration 
  - Press add.
  - Now in the repository overview, click install next to this repo.

## Install a Bluetooth Backend

Before configuring Home Assistant you need a Bluetooth backend and the MAC address of your basestation. Depending on your operating system, you may have to configure the proper Bluetooth backend for your system:

- On [Home Assistant](https://home-assistant.io/hassio/installation/): Will work out of the box.
- On [Home Assistant Container](https://home-assistant.io/docs/installation/docker/): Works out of the box with `--net=host` and properly configured Bluetooth on the host.
- On other Linux systems:
  - Install the `bluepy` library (via pip). When using a virtual environment, make sure to install the library in the right one.

## Scan for devices

Start a scan to determine the MAC addresses of your basestations (you can identify a basestation by looking for entries starting with `LHB-`, for example: `LHB-F27AE376`) using this command:

```bash
$ sudo hcitool lescan
LE Scan ...
1B:BE:05:0D:B0:5C (unknown)
F3:C7:68:BB:23:0B LHB-60B5777F
F7:8A:B0:FD:08:B5 LHB-F27AE376
[...]
```

Or, if your distribution is using bluetoothctl use the following commands:

```bash
$ bluetoothctl
[bluetooth]# scan on
[NEW] Controller <your Bluetooth adapter> [default]
[NEW] Device F3:C7:68:BB:23:0B LHB-60B5777F
```

If you can't use `hcitool` or `bluetoothctl` but have access to an Android phone you can try `BLE Scanner` or similar scanner applications from the Play Store to easily find your sensor MAC address. If you are using Windows 10, try the `Microsoft Bluetooth LE Explorer` app from the Windows Store.

## Configuration

To use your basestation(s) in your installation, add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
sensor:
  - platform: basestation
    mac: "xx:xx:xx:xx:xx:xx"
```

### More expansive example

Since you'll probably be adding more than 1 basestation, it's a good idea to use the [group integration](https://www.home-assistant.io/integrations/group) to group them together and control them all at once.

```yaml
group:
  basestations:
    name: Basestations
    entities:
      - switch.lhb_1
      - switch.lhb_2

switch:
  - platform: basestation
    mac: "xx:xx:xx:xx:xx:xx"
    name: "LHB 1"
  - platform: basestation
    mac: "xx:xx:xx:xx:xx:xx"
    name: "LHB 2"
```

## Automation ideas

- Turn the airco on when your VR equipment activates.
- Turn your basestations off/on when you turn off/on the lights
- Turn your basestations off if there's no motion detected in the room anymore.
- Start your computer (wake on lan), VR equipment, and screen (power plug) all at once.

## Final notes

- Yes, BLE does not conmmunicate well over long range.  
  If this integration becomes any popular, I'm willing to write a gateway app [like miflora has](https://github.com/ThomDietrich/miflora-mqtt-daemon) at some point.
- Largely inspired by [the miflora integration](https://github.com/home-assistant/core/tree/dev/homeassistant/components/miflora), thanks!
