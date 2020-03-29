import {CpuInfo} from "./cpu-info";
import {MemoryInfo} from "./memory-info";
import {DiskInfo} from "./disk-info";

export interface SystemInfo {
  cpuInfo: CpuInfo
  memoryInfo: MemoryInfo
  diskInfo: DiskInfo
}
