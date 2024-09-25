
from dataclasses import dataclass

@dataclass
class Rate:
    rate_str: str
    nominal: int
    drop: int 
    num: int
    den: int

    def generate_rate(rate_str):
        if rate_str == "23.976":
            return Rate("23.976", 24, 0, 24000, 1001)
        elif rate_str == "59.94":
            return Rate("59.94", 60, 4, 60000, 1001)
        elif rate_str == "29.97":
            return Rate("29.97", 30, 2, 30000, 1001)
        elif isinstance(rate_str, int):
            nominal = int(rate_str)
            return Rate(str(rate_str), nominal, 0, nominal, 1)
        else:
            raise ValueError("Unsupported rate string")

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

    def SubtractFrames(self, frames: int) -> None:
        self.frame -= frames