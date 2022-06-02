question = ["修改后是否可以闭源分发/使用其他许可证分发",\
    "需要附加修改说明文档",\
    "明确不授予商标权",\
    "专利许可",\
    "附加收费/免费的担保或责任声明",\
    "针对类库进行许可",\
    "多许可证兼容",\
    "是否具有传染性",\
    "是否对网络分发进行约束",\
    "是否明确云服务场景"]

# license = ["MIT","Zlib/libpng","3-BSD","Mulan PSL v2","ZPLv2.0","Apache v2.0","MPL v2.0","EPL v2.0","LGPL v2.0","LGPL v3.0","GPL v3.0","AGPL v3.0","Mulan PubL v2"]

# 分发代码：将该许可证下的原件或者复制件提供给第三方的行为
# 合并/修改代码：将开源软件中的整体/部分代码（无论修改与否）添加到自己的代码中从而构成
# 一个新作品,该作品在分发时必须提供源代码或源代码获取方式.
# 使用库：要求在编译或运行时通过链接（静态链接或动态链接）、导入等方式把开源代码与自己
# 的代码绑定在一起后,自己的代码分发时必须提供源代码或源代码获取方式.
# “传染性”：要求通过“合并/修改、使用库”等方式将开源代码整体或部分与自己的代码组合后,必
# 须使用与开源软件相同的许可证进行分发并禁止闭源分发.
# 网络分发：通过网络服务或计算机网络分发开源软件的行为.
GPLv2 = {
    'patent':0,
    # 'Distribute':1,
    "change/merge":1,
    'infectivity':1,
    'library':1,
    'Network distribution':0
    }
GPLv3 = {
    'patent':1,
    # 'Distribute':1,
    "change/merge":1,
    'infectivity':1,
    'library':1,
    'Network distribution':0
}
AGPLv3 = {
    'patent':1,
    # 'Distribute':1,
    "change/merge":1,
    'infectivity':1,
    'library':1,
    'Network distribution':1
}
LGPLv2 = {
    'patent':1,
    # 'Distribute':1,
    "change/merge":1,
    'infectivity':0,
    'library':0,
    'Network distribution':0
}
LGPLv3 = {
    'patent':1,
    # 'Distribute':1,
    "change/merge":1,
    'infectivity':0,
    'library':0,
    'Network distribution':0
}
EPLv1 = {
    'patent':1,
    # 'Distribute':1,
    "change/merge":1,
    'infectivity':0,
    'library':0,
    'Network distribution':0
}
EPLv2 = {
    'patent':1,
    # 'Distribute':1,
    "change/merge":1,
    'infectivity':0,
    'library':0,
    'Network distribution':0
}
MPLv11 = {
    'patent':1,
    # 'Distribute':1,
    "change/merge":1,
    'infectivity':0,
    'library':0,
    'Network distribution':0
}
MPLv2 = {
    'patent':1,
    # 'Distribute':1,
    "change/merge":1,
    'infectivity':0,
    'library':0,
    'Network distribution':0
}
MIT = {
    'patent':0,
    # 'Distribute':1,
    "change/merge":0,
    'infectivity':0,
    'library':0,
    'Network distribution':0
}
BSD2 = {
    'patent':0,
    # 'Distribute':1,
    "change/merge":0,
    'infectivity':0,
    'library':0,
    'Network distribution':0
}
BSD3 = {
    'patent':0,
    # 'Distribute':1,
    "change/merge":0,
    'infectivity':0,
    'library':0,
    'Network distribution':0
}
Apache = {
    'patent':1,
    # 'Distribute':1,
    "change/merge":0,
    'infectivity':0,
    'library':0,
    'Network distribution':0
}
ZPLv2 = {
    'patent':0,
    # 'Distribute':1,
    "change/merge":0,
    'infectivity':0,
    'library':0,
    'Network distribution':0
}
license = [GPLv2,GPLv3,AGPLv3,LGPLv2,LGPLv3,EPLv1,EPLv2,MPLv11,MPLv2,MIT,BSD2,BSD3,Apache,ZPLv2]