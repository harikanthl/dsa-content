// camcheck — opens the Brio 300 and pops the macOS Video Effects panel, so you can
// see for yourself whether "Background" is offered for this camera.
// Build: swiftc -O -o scripts/camcheck tools/camcheck.swift
import AVFoundation
import Foundation

setvbuf(stdout, nil, _IONBF, 0)   // unbuffered: print immediately, even when piped

let session = AVCaptureSession()
let disco = AVCaptureDevice.DiscoverySession(
    deviceTypes: [.external, .builtInWideAngleCamera],
    mediaType: .video, position: .unspecified)

guard let cam = disco.devices.first(where: { $0.localizedName.contains("Brio") })
             ?? disco.devices.first else {
    print("no camera found"); exit(1)
}

print("camera: \(cam.localizedName)")
guard let input = try? AVCaptureDeviceInput(device: cam) else {
    print("could not open the camera — grant Camera permission to your terminal in")
    print("System Settings > Privacy & Security > Camera, then rerun.")
    exit(1)
}
session.beginConfiguration()
session.sessionPreset = .hd1920x1080
if session.canAddInput(input) { session.addInput(input) }
session.commitConfiguration()
session.startRunning()

// Give the system a moment to register an active capture client.
Thread.sleep(forTimeInterval: 1.0)

func state() {
    print("""

      portrait (background blur)   \(cam.isPortraitEffectActive ? "ON " : "off")
      background replacement       \(cam.isBackgroundReplacementActive ? "ON " : "off")
      studio light                 \(cam.isStudioLightActive ? "ON " : "off")
    """)
}
state()

print("""

  Opening the Video Effects panel now.
  Look for a "Background" control. If it is there, this camera gets macOS
  background replacement with no green screen — click it and pick a gradient,
  an Apple image, or your own photo.

  Leave this running while you experiment. Press Ctrl-C when done.
""")
AVCaptureDevice.showSystemUserInterface(.videoEffects)

// Poll so you can watch the flags flip as you toggle things in the panel.
var last = ""
while true {
    let now = "\(cam.isPortraitEffectActive)\(cam.isBackgroundReplacementActive)\(cam.isStudioLightActive)"
    if now != last { last = now; state() }
    Thread.sleep(forTimeInterval: 0.5)
}
