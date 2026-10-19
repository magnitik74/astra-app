using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;

class Program {
    static void CropToFullBleed(string srcPath, string outPath, int cropInset) {
        using (var src = Image.FromFile(srcPath)) {
            int cropSize = src.Width - (cropInset * 2);
            int cropX = cropInset;
            int cropY = cropInset;

            using (var dest = new Bitmap(1024, 1024)) {
                using (var g = Graphics.FromImage(dest)) {
                    g.InterpolationMode = InterpolationMode.HighQualityBicubic;
                    g.PixelOffsetMode = PixelOffsetMode.HighQuality;
                    g.SmoothingMode = SmoothingMode.HighQuality;

                    var srcRect = new Rectangle(cropX, cropY, cropSize, cropSize);
                    var destRect = new Rectangle(0, 0, 1024, 1024);

                    g.DrawImage(src, destRect, srcRect, GraphicsUnit.Pixel);
                }
                dest.Save(outPath, ImageFormat.Png);
            }
        }
        Console.WriteLine("Successfully created: " + outPath);
    }

    static void Main() {
        string img1 = @"C:\Users\Александр\.gemini\antigravity\brain\8dc77ab2-b9dd-4a62-9311-ed7a2c195cb3\.user_uploaded\media_1792290949494_ab88f643.png";
        string img2 = @"C:\Users\Александр\.gemini\antigravity\brain\8dc77ab2-b9dd-4a62-9311-ed7a2c195cb3\.user_uploaded\media_1792291135580_3035af9c.png";

        string out1 = @"C:\Users\Александр\.gemini\antigravity\brain\8dc77ab2-b9dd-4a62-9311-ed7a2c195cb3\astra_icon_v1_fullbleed.png";
        string out2 = @"C:\Users\Александр\.gemini\antigravity\brain\8dc77ab2-b9dd-4a62-9311-ed7a2c195cb3\astra_icon_v2_fullbleed.png";

        // Кропаем внутренний квадрат без белых полей и скруглений маски
        CropToFullBleed(img1, out1, 142);
        CropToFullBleed(img2, out2, 142);
    }
}
