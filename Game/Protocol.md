# Protocol
## States
Handshaking, Configuration, Queue, Play

### Handshake
#### Handshake

| Packet ID | State |  Field Name  | Field Type | Note |
|:---------:|:-----:|:------------:|:----------:|:----:|
| 0x00 | Handshaking |             |            |      |

### Login
#### Login Start
| Packet ID | State | Field Name | Field Type |       Note       |
|:---------:|:-----:|:----------:|:----------:|:----------------:|
| 0x00 | Login |  PlayerID  |    UUID    | Unique Player ID |

#### Queue Position
| Packet ID | State | Field Name | Field Type | Note |
|:---------:|:-----:|:----------:|:----------:|:----:|
| 0x01 | Login |  Position  |    Int     |      |


### Play
#### Player Position And Look
| Packet ID | State | Field Name | Field Type | Note |
|:---------:|:-----:|:----------:|:----------:|:----:|
|   0x00    | Play |  X  |  Double  |      |
|           | Play |  Y  |  Double  |      |
|           | Play |  Yaw  |  Float  |      |

#### Canon Look
| Packet ID | State | Field Name | Field Type | Note |
|:---------:|:-----:|:----------:|:----------:|:----:|
|   0x01    | Play |  Yaw  |  Float  |      |

#### Bullet Spawn
| Packet ID | State | Field Name | Field Type | Note |
|:---------:|:-----:|:----------:|:----------:|:----:|
|   0x02    | Play |            |            |      |

#### Bullet Position
| Packet ID | State | Field Name | Field Type | Note |
|:---------:|:-----:|:----------:|:----------:|:----:|
|   0x03    | Play |  X  |  Double  |      |
|           | Play |  Y  |  Double  |      |

#### Bullet Destroy
| Packet ID | State | Field Name | Field Type | Note |
|:---------:|:-----:|:----------:|:----------:|:----:|
|   0x04    | Play |            |            |      |

#### Bullet Hit
| Packet ID | State | Field Name | Field Type | Note |
|:---------:|:-----:|:----------:|:----------:|:----:|
|   0x05    | Play |            |            |      |



