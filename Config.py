# coding: utf-8

# 图片及视频检测结果保存路径
save_path = 'save_data'

# 使用的模型路径
model_path = 'models/best.pt'

# 英文类别名（43 类，遵循 GB 5768 国标）
names = {
    # 禁令标志 (0-18)
    0: 'speed_limit_20', 1: 'speed_limit_30', 2: 'speed_limit_40',
    3: 'speed_limit_50', 4: 'speed_limit_60', 5: 'speed_limit_70',
    6: 'speed_limit_80', 7: 'speed_limit_100', 8: 'speed_limit_120',
    9: 'no_entry', 10: 'no_turn_left', 11: 'no_turn_right',
    12: 'no_u_turn', 13: 'no_overtaking', 14: 'no_honking',
    15: 'no_parking', 16: 'no_stopping', 17: 'weight_limit',
    18: 'height_limit',
    # 指示标志 (19-28)
    19: 'go_straight', 20: 'turn_left', 21: 'turn_right',
    22: 'turn_left_right', 23: 'u_turn', 24: 'roundabout',
    25: 'pedestrian_crossing', 26: 'bicycle_lane', 27: 'motorway',
    28: 'parking',
    # 警告标志 (29-38)
    29: 'crosswalk_warning', 30: 'curve_left', 31: 'curve_right',
    32: 'steep_hill', 33: 'road_work', 34: 'traffic_light_ahead',
    35: 'falling_rocks', 36: 'slippery_road', 37: 'school_zone',
    38: 'intersection',
    # 其他标志 (39-42)
    39: 'stop_sign', 40: 'yield_sign', 41: 'guide_sign',
    42: 'highway_sign'
}

# 中文类别名
CH_names = [
    # 禁令标志
    '限速20', '限速30', '限速40', '限速50', '限速60', '限速70',
    '限速80', '限速100', '限速120',
    '禁止通行', '禁止左转', '禁止右转', '禁止掉头', '禁止超车',
    '禁止鸣笛', '禁止停车', '禁止长停', '限重', '限高',
    # 指示标志
    '直行', '左转', '右转', '左右转', '掉头', '环岛',
    '人行横道', '非机动车道', '机动车道', '停车场',
    # 警告标志
    '注意行人', '左弯道', '右弯道', '陡坡', '施工路段',
    '注意信号灯', '注意落石', '路滑', '注意儿童', '十字路口',
    # 其他标志
    '停车让行', '减速让行', '指路标志', '高速公路标志'
]

# 类别分组（用于进度条显示）
category_groups = {
    '禁令标志': list(range(0, 19)),
    '指示标志': list(range(19, 29)),
    '警告标志': list(range(29, 39)),
    '其他标志': list(range(39, 43))
}
