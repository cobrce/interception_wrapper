from interception import  *

if __name__ == "__main__":
    intecept = interception()
    intecept.set_keyboard_filter(interception_filter_key_state.INTERCEPTION_FILTER_KEY_DOWN.value | interception_filter_key_state.INTERCEPTION_FILTER_KEY_UP.value)
    while True:
        try:
            device = intecept.wait()
            data = intecept.receive(device)
            if data.state == interception_key_state.INTERCEPTION_KEY_UP.value:
                print(intecept.get_hardware_id(device).decode())
                print(data.code)
            intecept.send(device,data)
        except Exception as e:
            print(e)