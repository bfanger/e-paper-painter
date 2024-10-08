export default function fileToImage(file: File): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file);
    const image = new Image();
    image.onerror = reject;
    image.onload = () => {
      resolve(image);
      URL.revokeObjectURL(url);
    };
    image.src = url;
  });
}
