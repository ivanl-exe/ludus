from ludus import *

if __name__ == '__main__':
    ludus = Ludus()
    #Orthographic Viewport
    viewport = Viewport(width = 10, height = 10)

    group = ludus.new_group()
    object = ludus.add_object(props = {'x': 1, 'y': 1}, gid = group)
    #ludus.detach_group(object, group)

    handle = open('test/objects.bin', 'wb')
    ludus.dump(handle)

    handle = open('test/objects.bin', 'rb')
    ludus.load(handle)

    print(*map(ludus.get, [group, object]), sep = ', ')

    viewport.position(x = 0, y = 0, z = 0)
    ludus.render(viewport)

    #ludus.remove_object(object)

    print(ludus.objects, ludus.groups, sep = '\n')