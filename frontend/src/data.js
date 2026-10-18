// Class order must match the training notebook (alphabetical folder order).
export const CLASSES = [
  {
    key: "glioma",
    name: "Glioma",
    text:
      "Gliomas arise from glial (supporting) cells of the brain or spinal cord. On MRI they often appear as irregular masses with less well-defined borders.",
  },
  {
    key: "meningioma",
    name: "Meningioma",
    text:
      "Meningiomas grow from the meninges, the membranes surrounding the brain. On MRI they typically appear as well-defined masses attached to the brain's outer surface.",
  },
  {
    key: "notumor",
    name: "No Tumor",
    text:
      "The model found no pattern resembling the three tumor classes it was trained on in this image.",
  },
  {
    key: "pituitary",
    name: "Pituitary Tumor",
    text:
      "Pituitary tumors develop in the pituitary gland at the base of the brain. On MRI they are usually seen as a mass near the center-bottom of the skull.",
  },
];

export const ARCHITECTURE = [
  { layer: "Input", detail: "128 x 128 x 3 (RGB)" },
  { layer: "Rescaling", detail: "1/255 (inside the model)" },
  { layer: "Conv2D + ReLU", detail: "16 filters, 3x3" },
  { layer: "MaxPooling2D", detail: "2x2" },
  { layer: "Conv2D + ReLU", detail: "32 filters, 3x3" },
  { layer: "MaxPooling2D", detail: "2x2" },
  { layer: "Conv2D + ReLU", detail: "64 filters, 3x3" },
  { layer: "MaxPooling2D", detail: "2x2" },
  { layer: "Flatten", detail: "" },
  { layer: "Dense + ReLU", detail: "64 units" },
  { layer: "Dropout", detail: "0.4" },
  { layer: "Dense + Softmax", detail: "4 units (output)" },
];

// Reported results from the existing Google Colab evaluation (not produced by this website).
export const REPORTED = {
  accuracy: "82.12%",
  testImages: "1,600",
  f1: [
    { name: "Glioma", value: 0.76 },
    { name: "Meningioma", value: 0.72 },
    { name: "No Tumor", value: 0.88 },
    { name: "Pituitary Tumor", value: 0.91 },
  ],
};
