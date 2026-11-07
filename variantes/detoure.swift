// detoure <entree> <masque.png> : masque de la personne (blanc = personne), même taille que l'entrée.
import Foundation
import Vision
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let inURL = URL(fileURLWithPath: CommandLine.arguments[1])
let outURL = URL(fileURLWithPath: CommandLine.arguments[2])
let src = CGImageSourceCreateWithURL(inURL as CFURL, nil)!
let img = CGImageSourceCreateImageAtIndex(src, 0, nil)!
let req = VNGeneratePersonSegmentationRequest()
req.qualityLevel = .accurate
req.outputPixelFormat = kCVPixelFormatType_OneComponent8
try VNImageRequestHandler(cgImage: img, options: [:]).perform([req])
var mask = CIImage(cvPixelBuffer: req.results!.first!.pixelBuffer)
mask = mask.transformed(by: CGAffineTransform(scaleX: CGFloat(img.width) / mask.extent.width,
                                               y: CGFloat(img.height) / mask.extent.height))
let cg = CIContext().createCGImage(mask, from: CGRect(x: 0, y: 0, width: img.width, height: img.height))!
let dest = CGImageDestinationCreateWithURL(outURL as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg, nil)
CGImageDestinationFinalize(dest)
