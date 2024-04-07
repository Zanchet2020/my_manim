from manim import *
import math

class Derivative(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 20, 2],
            x_length=12,
            y_length=6,
            tips=False,
            axis_config={"include_numbers": True}
        ).to_corner(DL).set_color(WHITE)

        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        def quadratica(x):
            return 0.1 * (x*3 - 13*x*2 + 59*x - 70) + 7 
        
        def secante(x, dx, t):
            x1 = x + dx
            y = quadratica(x)
            y1 = quadratica(x1)
            m = (y1 - y) / (x1 - x)
            return m * t - m*x1 + y1

        x_graph = ValueTracker(0.001)
        x = ValueTracker(4.5)
        dx = ValueTracker(2)
        funct = always_redraw(lambda: axes.plot(quadratica, color=BLUE, x_range=[0, x_graph.get_value()]))

        secant = always_redraw(lambda: axes.plot(lambda t: secante(x.get_value(), dx.get_value(), t), color=RED_C))

        dot_x_dx = always_redraw(lambda: Dot(point=axes.c2p(x.get_value() + dx.get_value(), funct.underlying_function(x.get_value())), radius=0.07, color=ORANGE))

        dot1 = always_redraw(lambda: Dot(point=axes.c2p(x_graph.get_value(), funct.underlying_function(x_graph.get_value())), radius=0.05, color=BLUE))
        
        dot_x = always_redraw(
            lambda: Dot(
                point=axes.c2p(x.get_value(),
                               funct.underlying_function(x.get_value())),
                               radius=0.08,
                               color=ORANGE)
        )
        dot_dx = always_redraw(
            lambda: Dot(
                point=axes.c2p(x.get_value() + dx.get_value(),
                               funct.underlying_function(x.get_value()+dx.get_value())),
                               radius=0.08,
                               color=ORANGE)
        )

        dx_line = always_redraw(
            lambda: Line(
                axes.c2p(
                    x.get_value(), 
                    funct.underlying_function(x.get_value())
                ), 
                axes.c2p(
                    x.get_value() + dx.get_value(), 
                    funct.underlying_function(x.get_value())
                ),
                color=YELLOW
            )
        )
        dy_line = always_redraw(
            lambda: Line(
                axes.c2p(
                    dx.get_value() + x.get_value(), 
                    funct.underlying_function(x.get_value() + dx.get_value())
                ), 
                axes.c2p(
                    x.get_value() + dx.get_value(), 
                    funct.underlying_function(x.get_value())
                ),
                color=YELLOW
            )
        )

        decimal_opacity = ValueTracker(1)

        dy_dx = always_redraw(
            lambda: MathTex("\\frac{dy}{dx}").next_to(
                axes.c2p(x.get_value(), funct.underlying_function(x.get_value())),
                direction=UP
            ).set_opacity(1 - decimal_opacity.get_value())
        )
        

        dy_bracket = always_redraw(
            lambda: Brace(dy_line, RIGHT)
        )

        dx_bracket = always_redraw(
            lambda: Brace(dx_line, DOWN)
        )

        dx_value = always_redraw(
            lambda: MathTex(
                "\\Delta X &= ",
                "{:.2f}".format(dx.get_value()),
                fill_opacity=decimal_opacity.get_value()
            ).next_to(dx_bracket, direction=DOWN)
        )
        
        dy_value = always_redraw(
            lambda: MathTex(
                "\\Delta Y &= ",
                "{:.2f}".format(
                    funct.underlying_function(x.get_value() + dx.get_value()) - funct.underlying_function(x.get_value())
                ),
                fill_opacity=decimal_opacity.get_value()
            ).next_to(dy_bracket, direction=RIGHT)
        )

        self.add(dy_dx)
        self.add(funct)
        self.wait(1)
        self.play(
            AnimationGroup(Write(axes), Write(axes_labels))
        )
        self.wait(0.6)
        self.play(FadeIn(dot1),run_time=0.2)
        self.play(x_graph.animate.set_value(10), run_time=1.2)
        # self.play(FadeOut(dot1),run_time=0.2)

        self.wait(0.4)

        self.play(AnimationGroup(
            Create(dx_value),
            Create(dy_value),
            Create(dx_bracket),
            Create(dy_bracket),
            Create(dx_line),
            Create(dy_line),
            FadeIn(dot_x),
            FadeIn(dot_dx),
            FadeIn(dot_x_dx)
        ), run_time=0.3)

        self.wait(0.2)
        self.play(Write(secant), run_time=0.4)
        
        self.play(x.animate.set_value(7), run_time=1.5)
        self.wait(0.4)

        self.play(
            AnimationGroup(
                dx.animate.set_value(0.00001),
                decimal_opacity.animate.set_value(0)
            ), run_time=1.5)


        self.play(x.animate.set_value(2), run_time=1.5)
    
        self.play(AnimationGroup(
            x.animate.set_value(4.5),
            dx.animate.set_value(3),
            decimal_opacity.animate.set_value(1),
            run_time=1.5,
            lag_ratio=0.2
        ))

        self.wait(1)