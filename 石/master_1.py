import canopen
import time

# 初始化主站网络
network = canopen.Network()
network.connect(channel="vcan0", bustype="socketcan", bitrate=125000)

# 添加主站节点（节点ID=1，假设已配置对象字典）
master_node = network.add_node(1, "Slaver.eds")

# 配置 TPDO1（发送PDO到从站）
# 目标：将数据发送到从站（节点2）的 RPDO1（COB-ID = 0x200 + 2 = 0x202）
master_node.tpdo[1].clear()
master_node.tpdo[1].cob_id = 0x2002  # 设置目标COB-ID为从站的RPDO1
master_node.tpdo[1].add_variable(".Arc_MegmeetCANInitDataCase.WorkMode")  # 假设对象字典中定义了一个变量（如0x3000:0x01，类型INT32）
master_node.tpdo[1].trans_type = 255  # 异步传输
master_node.tpdo[1].enabled = True
master_node.tpdo[1].save()  # 保存配置到节点

# 启动主站节点
master_node.tpdo[1].start(0.1)
master_node.nmt.state = 'OPERATIONAL'

try:
    counter = 0
    while True:
        # 更新要发送的数据（例如递增的计数器）
        master_node.tpdo[1][".Arc_MegmeetCANInitDataCase.WorkMode"].raw = counter
        master_node.tpdo[1].transmit()
        s = master_node.tpdo[1][".Arc_MegmeetCANInitDataCase.WorkMode"].raw
        print(f"主站发送数据: {s}")
        counter += 1
        time.sleep(1)
except KeyboardInterrupt:
    network.disconnect()