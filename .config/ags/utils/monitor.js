import Gdk from 'gi://Gdk';

const display = Gdk.Display.get_default()

export const get_active_monitor_num = () => {
    const screen = display.get_default_screen()
    const pointer = display.get_device_manager().get_client_pointer()

    const [pointerX, pointerY] = pointer.get_position()

    return screen.get_monitor_at_point(pointerX, pointerY)
}