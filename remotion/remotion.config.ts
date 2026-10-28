import path from "node:path";
import { Config } from "@remotion/cli/config";

// Las fotos y el audio viven en produccion/<video>/ y se referencian con staticFile("<video>/...").
Config.setPublicDir(path.join(process.cwd(), "..", "produccion"));
Config.setVideoImageFormat("jpeg");
Config.setJpegQuality(92);
Config.setCodec("h264");
Config.setCrf(18);
Config.setPixelFormat("yuv420p");
Config.setColorSpace("bt709");
Config.setConcurrency(6);
