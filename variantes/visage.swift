// Affiche "x y w h" (pixels, origine en haut à gauche) du plus grand visage de l'image.
import Foundation
import Vision
import ImageIO

let url = URL(fileURLWithPath: CommandLine.arguments[1])
guard let src = CGImageSourceCreateWithURL(url as CFURL, nil),
      let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { exit(2) }
let req = VNDetectFaceRectanglesRequest()
try VNImageRequestHandler(cgImage: img, options: [:]).perform([req])
guard let face = (req.results ?? []).max(by: { $0.boundingBox.width < $1.boundingBox.width }) else { exit(1) }
let b = face.boundingBox
let W = Double(img.width), H = Double(img.height)
print(Int(b.minX * W), Int((1 - b.maxY) * H), Int(b.width * W), Int(b.height * H))
