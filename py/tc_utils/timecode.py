
from dataclasses import dataclass

@dataclass
class Rate:
    rate_str: str
    nominal: int
    drop: int 
    num: int
    den: int

Rate_24 = Rate("24", 24, 0, 24, 1)
Rate_25 = Rate("25", 25, 0, 25, 1)
Rate_30 = Rate("30", 30, 0, 30, 1)
Rate_29_97 = Rate("29.97", 30, 2, 30000, 1001)
Rate_50 = Rate("50", 50, 0, 50, 1)
Rate_59_94 = Rate("59.94", 60, 4, 60000, 1001)
Rate_60 = Rate("60", 60, 0, 60, 1)
Rate_23_976 = Rate("23.976", 24, 0, 24000, 1001)

@dataclass
class Components:
    hours: int
    minutes: int
    seconds: int
    frames: int

def truncate(f, n):
    return int(f * 10 ** n) / 10 ** n
@dataclass
class Timecode:
    rate: Rate
    frame: int
    drop_frame: bool

    def Frame(self):
        return self.frame

    def Seconds(self) -> float:
        if self.rate.rate_str == "29.97":
            return truncate(float(self.frame) * self.rate.den / self.rate.num, 5)
        elif self.rate.rate_str == "59.94":
            return truncate(float(self.frame) * self.rate.den / self.rate.num, 5)
        elif self.rate.rate_str == "23.976":
            return truncate(float(self.frame) * self.rate.den / self.rate.num, 5)
        else:
            return truncate(float(self.frame) / float(self.rate.nominal), 5)

    # def Seconds(self) -> float:
    #     if self.rate.rate_str == "29.97":
    #         return float(self.frame) / 29.97 
    #     elif self.rate.rate_str == "59.94":
    #         return float(self.frame) / 59.94
    #     elif self.rate.rate_str == "23.976":
    #         return float(self.frame) / 23.976
    #     else:
    #         return float(self.frame) / float(self.rate.nominal)
        
    def componentNDF(self, frame: int) -> Components:
        hh = frame // (3600 * self.rate.nominal)
        mm = (frame // (60 * self.rate.nominal)) % 60
        ss = (frame // self.rate.nominal) % 60
        ff = frame % self.rate.nominal
        return Components(hh, mm, ss, ff)
    

    def componentsDF(self, frame: int) -> Components:
        comps = self.componentNDF(frame)

        mins_crossed = comps.hours * 60 + comps.minutes
        drop_incidents = mins_crossed - (mins_crossed // 10)

        while drop_incidents > 0:
            frame += self.rate.drop * drop_incidents
            new_comps = self.componentNDF(frame)

            drop_incidents = 0 

            for m in range(comps.hours * 60 + comps.minutes + 1, (new_comps.hours * 60 + new_comps.minutes) + 1):
                if (m % 10) > 0:
                    drop_incidents += 1

            comps = new_comps
        return comps


    def Components(self) -> Components:
        if self.drop_frame:
            return self.componentsDF(self.frame)
        else:
            return self.componentNDF(self.frame)

        
    def String(self) -> str:
        comps = self.Components()
        sep = ";" if self.drop_frame else ":"
        return f"{comps.hours:02d}:{comps.minutes:02d}:{comps.seconds:02d}{sep}{comps.frames:02d}"

    def Equals(self, other) -> bool:
        return self.rate == other.rate and self.frame == other.frame and self.drop_frame == other.drop_frame

    def AddFrames(self, frames: int) -> None:
        self.frame += frames
        




