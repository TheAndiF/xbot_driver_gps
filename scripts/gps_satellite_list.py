#!/usr/bin/env python3
import rospy
from xbot_msgs.msg import GnssSatelliteArray

TOPIC = "/ll/position/gps/satellites"


def fmt_bool(value):
    return "yes" if value else "no"


def cb(msg):
    used = sum(1 for sat in msg.satellites if sat.used)
    print("\033c", end="")
    print(f"GPS satellites from {TOPIC}")
    print(f"stamp: {msg.header.stamp.to_sec():.3f} | sensor_stamp: {msg.sensor_stamp} | visible: {msg.num_svs} | used: {used}")
    print()
    print("GNSS      SV   USED  C/N0  ELEV  AZIM   PRRES  QUAL")
    print("------------------------------------------------------")
    for sat in sorted(msg.satellites, key=lambda s: (s.gnss, s.sv_id)):
        print(f"{sat.gnss:<9} {sat.sv_id:>3}  {fmt_bool(sat.used):<4}  {sat.cno:>4}  {sat.elev:>4}  {sat.azim:>5}  {sat.pr_res:>6}  {sat.quality_ind:>4}")


def main():
    rospy.init_node("gps_satellite_list", anonymous=True)
    rospy.Subscriber(TOPIC, GnssSatelliteArray, cb, queue_size=1)
    print(f"Waiting for {TOPIC} ...")
    rospy.spin()


if __name__ == "__main__":
    main()
