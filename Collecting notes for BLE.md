# Collecting Notes for BLE

## Definitions

[BLE](https://learning.oreilly.com/library/view/getting-started-with/9781491900550/pr01.html#_how_to_use_this_book) - 

**Bluetooth Low Energy**, introduced as part of Bluetooth 4.0 spec'. 

Introduced in 2010. Developed by Nokia (as Wibree), with significant input from Apple Inc.

[GATT](https://learn.adafruit.com/introduction-to-bluetooth-low-energy/gatt) - 

**Generic ATTribute** Profile. The method of data exchange. This is a generic profile used when no specific profile exists for the application data (eg. diabetes devices use the Glucose Profile).

HCI - 

Host Controller Interface

Protocol - 

The "building blocks" of all spec compliant devices. Implentations of routing, formatting, encode/decode, etc.

Profiles -

Vertical slices covering operational scenarios. GAP and GATT are both generic profiles. Proximity Profile and Glucose Profile are further specific examples.

## Bluetooth Standards

## 4.0

*2010 Spec*

BR / EDR (classic bluetooth) defines the standard since 1.0 onward.
BLE, is the lower power spec introduced in this revision.

Two types can be used with the above conf's, Single or Dual mode. Single implements only BLE and may only communicate with other BLE compliant devices. Dual mode may communicate with either BR / EDR or BLE devices.

Dual mode is often referred to as "Smart Ready" while single is simply "Smart". Previous revision spec's are then "Classic".

#### 4.1

*2013 Spec* The current BLE reference standard. 

# Profiles

## GAP (Advertisment and Connections)

Low level radio protocols. It defines roles, procedures and modes for devices to broadcast, discover, establish, and manage connections, as well as negotiate security. GAP is the most generic vertical slice available to BLE devices.

## GATT (Services and Characteristics)

GATT relates specifically to data-exchange. Inclusive of discover, read/write, and push exchange operations. It, like, GAP, is a generic vertical slice available to BLE devices.

## Protocol Basics

* Modulation rate: 1Mbps, ie. *theoretical* upper limit.
* Relies on short packet bursts and "race to idle" design.
* It is possible for BLE to support > 30m LoS. However the power draw at this range is significant for the low-energy requirement. 2 - 5m is more typical.

### Radio (PHYS layer)

BLE utilises a 2.4GHz (Ind, Sci, Med) band to communicate. The band is 40 channels on the range [2.4000 -2.4835] GHz. 37 of these 40 are for connection data, the remaining 3 (37, 38, and 39) are advertising channels for broadcast operations.

### Device Addresses

The address is similar to an Ethernet MAC address. A 48b (6B) uuid that is unique among peers. Two types exist,

1. Pub : fixed BR/EDR factory-programmed address which is IEEE registerd per lifetime.
2. Rand: preprogrammed, or runtime dynamic.

### Scanning

* Active : issues a scan req packet after receiving an advert packet. Advertiser response with a scan response packet.
* Passive: Listen for any advert packets. No transmissions.

White lists and blacklists exist.

## Hardware Configurations

#### SoC - single IC runs the app, host, and, controller

#### Dual IC over HCI - an IC runs the app and host, then uses HC with a further IC to run the controller. Any host may be combined with any controller this way.

#### Dual IC with connectivity device - One IC runs teh app and uses a propietary protocol to communicate with a second IC running the host + controller stack.

## Network Topology

*Broadcast* or *Connection* both subject to GAP profile.

### Broadcast and Observe (Uni-directional transfer)

Connectionlesss broadcasting, send to any listening scanner within range. Scanners are observers in this pattern. Broadcasters are BLE controllers. 

* This takes advantage of the advertising spec' built-in to BLE.
* A standard advertising packet contains a 31b payload, 
* a secondary scan-response may include a further 31b payload if required

## Direct Connection (Bi-directional transfer)

A central (master) and peripheral (slave) device pattern.

* The previously mentioned advertisment alerts observers of potential connections.
* Observer sends a connection request to the broadcaster, creating a direct connection.
* It is possible to act as a central and peripheral simultaneously.
* A central may connect many peripherals and *vice versa*.