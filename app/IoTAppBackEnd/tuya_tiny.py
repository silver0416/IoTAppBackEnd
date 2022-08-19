import json
import tinytuya

d= tinytuya.OutletDevice('566855732462ab16d7a4', '192.168.100.10',"keyf9fsmuufeywsr")
d.set_version(3.3)
data = d.status()
command = {
    "control": "send",
    "head": "020ec400000000000500130026004c00990b7b",
    "key1": "02%%0018F2A0D5@^",
    "type": 0.00,
    "delay": 300
    
}
payload = d.generate_payload(tinytuya.CONTROL, {"201": json.dumps(command)})
d.send(payload)
