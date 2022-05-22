import pygame
from pygame.locals import *
from pathFinder import Dijkstra, Heuristic, Astar
from os.path import join
from cmath import inf

class App:
    def __init__(self, size, fps, table_w, table_h, tile, pos) -> None:
        self.size = size
        self.fps = fps
        self.show_data = False
        self.resolve = False
        self.path = []
        self.method = 'Dij'
        self.save_ct = 0

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        font = pygame.font.match_font('consolas')
        self.font = pygame.font.Font(font, 20)

        self.state = 0
        self.start_pos = None
        self.end_pos = None
        self.table = [[0 for x in range(table_w)] for y in range(table_h)]
        self.tile = tile
        self.table_surf = pygame.Surface((table_w*tile, table_h*tile))
        self.table_rect = self.table_surf.get_rect(topleft=pos)

        self.chose_method()

        self.table_surf_update()
    
    def chose_method(self):
        match self.method:
            case 'Dij':
                self.pathfider = Dijkstra(self.table, self.end_pos)
            case 'Heu':
                self.pathfider = Heuristic(self.table, self.end_pos)
            case 'As':
                self.pathfider = Astar(self.table, self.end_pos)

    def add_data(self, x, y, center):
        match self.method:
            case 'Dij':
                text = f'{self.pathfider.graph[y][x].path_sum}'
            case 'Heu':
                d = self.pathfider.graph[y][x].distance
                if d != inf:
                    d = round(d)
                text = f'{ d }'
            case 'As':
                d = self.pathfider.graph[y][x].distance + self.pathfider.graph[y][x].path_sum
                if d != inf:
                    d = round(d)
                text = f'{ d }'
    
        surf_text = self.font.render(text, True, (100,100,100))
        rect_text = surf_text.get_rect(center=center)
        self.table_surf.blit(surf_text, rect_text)

    def table_surf_update(self) -> None:
        self.table_surf.fill((0,0,0))

        if self.start_pos:
            x, y = self.start_pos
            rect = (x*self.tile, y*self.tile, self.tile, self.tile)
            pygame.draw.rect(self.table_surf, (0,0,200), rect, 0)
        if self.end_pos:
            x, y = self.end_pos
            rect = (x*self.tile, y*self.tile, self.tile, self.tile)
            pygame.draw.rect(self.table_surf, (0,200,0), rect, 0)

        path = [(0,0)]*len(self.path)
        visited = [v.value for v in self.pathfider.visited]
        for y in range( len(self.table) ):
            for x in range( len(self.table[0]) ):
                rect = pygame.Rect((x*self.tile, y*self.tile, self.tile, self.tile))
                if self.table[y][x] == 0:
                    pygame.draw.rect(self.table_surf, (100,100,100), rect, 1)
                else:
                    pygame.draw.rect(self.table_surf, (100,100,100), rect, 0)

                if self.show_data:
                    self.add_data(x, y, rect.center)

                if (x,y) in self.path:
                    i = self.path.index((x,y))
                    path[i] = rect.center
                if (x,y) in visited:
                    pygame.draw.rect(self.table_surf, (0,150,0), rect, 2)
        if len(path) > 1:
            pygame.draw.lines(self.table_surf, (255,255,0), False, path, 5)

    def table_mouse_pos(self) -> tuple[int, int]:
        mx, my = pygame.mouse.get_pos()
        tx, ty = self.table_rect.topleft

        px, py = (mx-tx)//self.tile, (my-ty)//self.tile
        if 0 <= px < len(self.table[0]) and 0 <= py < len(self.table):
            return px, py
    
    def save(self):
        name = f'sol_{self.save_ct}_{self.method}.png'
        path = join('img', name)
        pygame.image.save(self.table_surf, path)
        self.save_ct += 1
        print(f'Image saved: {name}')

    def mouse_events(self) -> None:
        press = pygame.mouse.get_pressed()
        if press[0]:
            pos = self.table_mouse_pos()
            if pos:
                if self.state == 2:
                    self.start_pos = pos
                    self.pathfider.set_start(pos)
                    self.restart()
                elif self.state == 3:
                    self.end_pos = pos
                    self.path = self.pathfider.get_path(self.end_pos)
                else:
                    x, y = pos
                    self.table[y][x] = self.state
                    self.restart()
    
    def restart(self):
        self.chose_method()
        if self.start_pos:
            self.pathfider.set_start(self.start_pos)
        self.path = []

    def key_event(self) -> None:
        for event in pygame.event.get(KEYUP):
            if event.key in (K_0, K_KP_0):
                self.state = 0
            elif event.key in (K_1, K_KP_1):
                self.state = 1
            elif event.key in (K_2, K_KP_2):
                self.state = 2
            elif event.key in (K_3, K_KP_3):
                self.state = 3
            elif event.key in (K_m,):
                self.show_data = not self.show_data
            elif event.key in (K_s,):
                self.pathfider.step()
            elif event.key in (K_SPACE,):
                self.restart()
                self.resolve = True
            elif event.key in (K_r,):
                self.restart()
            elif event.key in (K_f,):
                self.save()
            elif event.key in (K_F1,):
                self.method = 'Dij'
                self.restart()
                print('Method: Dijkstra')
            elif event.key in (K_F2,):
                self.method = 'Heu'
                self.restart()
                print('Method: Heuristic')
            elif event.key in (K_F3,):
                self.method = 'As'
                self.restart()
                print('Method: As')
    
    def write(self, text:str, center:tuple[int, int]) -> None:
        surf = self.font.render(text, True, (255,255,255), (0,0,0))
        rect = surf.get_rect(center=center)
        self.screen.blit(surf, rect)

    def run(self) -> None:
        run = True
        n = 0
        while run:
            self.screen.fill((50,50,50))
            if self.resolve:
                self.resolve = self.pathfider.step()
                n += 1
            elif self.end_pos:
                self.path = self.pathfider.get_path(self.end_pos)
                if n:
                    print(f'Steps to Find a Solution: {n}\nSolution Lenght Path: {len(self.path)}\n')
                n = 0
            self.table_surf_update()
            self.screen.blit(self.table_surf, self.table_rect)
            self.write(f'fps = {round(self.clock.get_fps())}', (100,50))
            self.key_event()
            self.mouse_events()
            pygame.display.flip()
            self.clock.tick(self.fps)

            if pygame.event.get(QUIT):
                run = False
        pygame.quit()
            

def main() -> None:
    app = App( size=(1000,1000), fps=60, table_w=30, table_h=30, tile=30, pos=(20,70) )
    #app = App( (1000,900), 60, 10, 10 , 60, (20,70) )
    app.run()

if __name__ == '__main__':
    main()
