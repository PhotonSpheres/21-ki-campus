from manim import *
from manim.opengl import *

from tensorflow.keras.datasets import mnist
(X_train, Y_train), (X_test, Y_test) = mnist.load_data()

sample_num = 2
sample = X_train[sample_num].flatten()

class NNInput(ZoomedScene):

    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=4,
            zoomed_display_width=4,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
            },
            **kwargs
        )


    def construct(self):

        # self.camera.background_color = "#ece6e2"

        back_rec = Rectangle(
            width=20,
            height=9,
            color=WHITE,
            fill_opacity=1
        ).set_z_index(-1)
        self.add(back_rec)
        
        pixel_array = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=1,
            ) for _ in range(28*28)]
        ).arrange_in_grid().scale(0.1).to_edge(UP)

        pixel_array_empty = pixel_array.copy()

        b1 = Brace(pixel_array, DOWN).set_color(BLACK)
        b2 = Brace(pixel_array, LEFT).set_color(BLACK)

        b1text = b1.get_text("28").set_color(BLACK)
        b2text = b2.get_text("28").set_color(BLACK)

        numbers = VGroup()


        for k in range(28*28):

            opacity_number = sample[k]/255

            num = DecimalNumber(
                opacity_number,
                num_decimal_places=1,
            ).scale(0.25).set_color(GREEN)

            pixel_array[k].set_style(
                fill_opacity=opacity_number
            )

            #pixel_array[k].add(num)
            num.move_to(pixel_array[k].get_center())
            numbers.add(num)

        self.play(
            FadeIn(pixel_array_empty)
        )
        self.wait(0.5)

        self.play(
            DrawBorderThenFill(b1),
            DrawBorderThenFill(b2),
            Write(b1text),
            Write(b2text)
        )
        self.wait()

        self.play(
            ReplacementTransform(pixel_array_empty, pixel_array),
        )
        self.play(
            FadeIn(numbers)
        )
        self.wait()

        self.play(
            VGroup(b1,b2,b1text,b2text,pixel_array,numbers).animate.to_edge(LEFT)
        )
        self.wait()

        for mob in pixel_array:
            mob.add_updater(lambda x: x)

        self.activate_zooming(animate=True)
        self.wait(0.5)

        self.play(
            self.zoomed_camera.frame.animate.shift( 4*LEFT ),
            rate_func=linear,
            run_time=10
        )

        # self.play(self.zoomed_camera.frame.animate.shift(0.5 * (2.8*LEFT+DOWN)))

        self.wait()

class SquareToLayer(Scene):
    def construct(self):

        self.camera.background_color = WHITE

        pixel_array = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=1,
            ) for _ in range(28*28)]
        ).arrange_in_grid().scale(0.1).to_edge(UP)

        b1 = Brace(pixel_array, DOWN).set_color(BLACK)
        b2 = Brace(pixel_array, LEFT).set_color(BLACK)

        b1text = b1.get_text("28").set_color(BLACK)
        b2text = b2.get_text("28").set_color(BLACK)

        numbers = VGroup()


        for k in range(28*28):

            opacity_number = sample[k]/255

            num = DecimalNumber(
                opacity_number,
                num_decimal_places=1,
            ).scale(0.25).set_color(GREEN)

            pixel_array[k].set_style(
                fill_opacity=opacity_number
            )

            #pixel_array[k].add(num)
            num.move_to(pixel_array[k].get_center())
            numbers.add(num)

        VGroup(b1,b2,b1text,b2text,pixel_array,numbers).to_edge(LEFT)

        self.add(
            VGroup(b1,b2,b1text,b2text,pixel_array,numbers)
        )
        self.wait()

        headline = Tex(r"\texttt{Input-Layer}").to_edge(UP).set_x(4).set_color(BLACK)

        self.play(
            Write(headline)
        )
        self.wait()

        dots = VGroup(
            Dot(color=BLACK).move_to([4,-0.25,0]),
            Dot(color=BLACK).move_to([4,0.375,0]),
            Dot(color=BLACK).move_to([4,-0.875,0]),
        )

        self.play(
            LaggedStart(
                FadeOut(b1,b2,b1text,b2text),
                AnimationGroup(
                    pixel_array[0].animate.scale(2).move_to([4,2.5,0]),
                    numbers[0].animate.scale(2).move_to([4,2.5,0]),
                    pixel_array[-1].animate.scale(2).move_to([4,-3,0]),
                    numbers[-1].animate.scale(2).move_to([4,-3,0]),
                ),
                AnimationGroup(
                    pixel_array[1].animate.scale(2).move_to([4,2,0]),
                    numbers[1].animate.scale(2).move_to([4,2,0]),
                    pixel_array[-2].animate.scale(2).move_to([4,-2.5,0]),
                    numbers[-2].animate.scale(2).move_to([4,-2.5,0]),
                ),
                AnimationGroup(
                    pixel_array[2].animate.scale(2).move_to([4,1.5,0]),
                    numbers[2].animate.scale(2).move_to([4,1.5,0]),
                    pixel_array[-3].animate.scale(2).move_to([4,-2,0]),
                    numbers[-3].animate.scale(2).move_to([4,-2,0]),
                ),
                AnimationGroup(
                    pixel_array[3].animate.scale(2).move_to([4,1,0]),
                    numbers[3].animate.scale(2).move_to([4,1,0]),
                    pixel_array[-4].animate.scale(2).move_to([4,-1.5,0]),
                    numbers[-4].animate.scale(2).move_to([4,-1.5,0]),
                ),
                AnimationGroup(
                    ReplacementTransform(
                        VGroup(pixel_array[4:-4], numbers[4:-4]),
                        dots
                    )
                ),
                lag_ratio=0.8
            )
        )
        self.wait()

        self.play(
            headline.animate.set_x(0),
            dots.animate.set_x(0),
            pixel_array[0:4].animate.set_x(0),
            pixel_array[-4:].animate.set_x(0),
            numbers[0:4].animate.set_x(0),
            numbers[-4:].animate.set_x(0),
        )
        self.wait()

        b = Brace(
            VGroup(pixel_array[0], pixel_array[-1]),
            RIGHT
        ).set_color(BLACK)
        btext = b.get_text("28x28=784").set_color(BLACK)

        self.play(
            Write(b),
            Write(btext)
        )
        self.wait()


# config["pixel_height"] = 1920
# config["pixel_width"] = 1920
# config["frame_height"] = 16.0
# config["frame_width"] = 16.0


class SquareToLayer2_eng(Scene):
    def construct(self):

        self.camera.background_color = WHITE

        pixel_array = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=1,
            ) for _ in range(28*28)]
        ).arrange_in_grid().scale(0.1)

        b1 = Brace(pixel_array, DOWN).set_color(BLACK)
        b2 = Brace(pixel_array, LEFT).set_color(BLACK)

        b1text = b1.get_text("28").set_color(BLACK)
        b2text = b2.get_text("28").set_color(BLACK)

        numbers = VGroup()


        for k in range(28*28):

            opacity_number = sample[k]/255

            num = DecimalNumber(
                opacity_number,
                num_decimal_places=1,
            ).scale(0.25).set_color(GREEN)

            pixel_array[k].set_style(
                fill_opacity=opacity_number
            )

            #pixel_array[k].add(num)
            num.move_to(pixel_array[k].get_center())
            numbers.add(num)

        VGroup(b1,b2,b1text,b2text,pixel_array,numbers).scale(0.8).to_edge(LEFT)

        self.add(
            VGroup(b1,b2,b1text,b2text,pixel_array,numbers)
        )
        self.wait()

        # headline = Tex(r"\texttt{Input-Layer}").scale(0.7).to_edge(UP, buff=0.2).set_x(4).set_color(BLACK)
        headline = Tex(r"\texttt{Input layer}").scale(0.7).to_edge(UP, buff=0.2).set_x(4).set_color(BLACK)

        self.play(
            Write(headline)
        )
        self.wait()

        self.play(
            FadeOut(numbers,b1,b1text,b2,b2text)
        )
        self.wait()

        input_1 = VGroup(*pixel_array[0:28].copy()).arrange(DOWN, buff=0.05).scale(0.6).set_x(4).next_to(headline, DOWN)
        input_2 = VGroup(*pixel_array[28:2*28].copy()).arrange(DOWN, buff=0.05).scale(0.6).set_x(4).next_to(input_1, DOWN, buff=0.05)
        input_3 = VGroup(*pixel_array[2*28:3*28].copy()).arrange(DOWN, buff=0.05).scale(0.6).set_x(4)

        length = input_1.get_top()[1] - input_1.get_bottom()[1]
        d1 = config["frame_height"]/2 - input_1.get_top()[1]

        self.play(
            ReplacementTransform(
                pixel_array[0:28],
                input_1
            )
        )
        self.wait()

        self.play(
            ReplacementTransform(
                pixel_array[28:2*28],
                input_2
            )
        )
        self.wait(0.5)

        self.play(
            headline.animate.shift(LEFT*2)
        )

        self.play(
            VGroup(input_1,input_2).animate.shift(UP*length),
        )
        input_3.next_to(input_2, DOWN, buff=0.05)
        self.play(
            ReplacementTransform(
                pixel_array[2*28:3*28],
                input_3
            )
        )
        self.wait(0.4)

        all_inputs = VGroup(input_1,input_2,input_3)

        run_time_func = lambda x: -0.3*np.exp( (- (x-16)**2) / (80) ) + 0.5

        for k in range(4,29):
            input_k = VGroup(*pixel_array[(k-1)*28:k*28].copy()).arrange(DOWN, buff=0.05).scale(0.6).set_x(4)

            self.play(
                all_inputs.animate.shift( UP * (length+0.05) ),
                run_time=run_time_func(k)
            )

            input_k.next_to(all_inputs[-1], DOWN, buff=0.05)

            self.play(
                ReplacementTransform(
                    pixel_array[(k-1)*28:k*28],
                    input_k
                ),
                run_time=run_time_func(k)
            )

            all_inputs.add(input_k)


        self.wait()

        dots = VGroup(
            Dot(color=BLACK).scale(0.4),
            Dot(color=BLACK).scale(0.4),
            Dot(color=BLACK).scale(0.4),
        ).arrange(DOWN, buff=0.3)

        self.play(
            headline.animate.set_x(0),
        )

        self.play(
            input_1[0:20].animate.next_to(headline, DOWN),
            all_inputs[-1][8:].animate.set_x(0).to_edge(DOWN, buff=d1),
            ReplacementTransform(
                VGroup(input_1[20:], all_inputs[1:-1], all_inputs[-1][0:8]),
                dots
            ),
            run_time=2
        )
        self.wait()

        b = Brace(
            VGroup(input_1[0], all_inputs[-1][-1]),
            RIGHT
        ).set_color(BLACK)

        btext = b.get_tex(r"28 \times 28=784").set_color(BLACK)

        self.play(
            Write(b),
            Write(btext)
        )
        self.wait()


class FullNN_eng(Scene):
    def construct(self):

        self.camera.background_color = WHITE

        d_buffer = 1

        # text_input = Tex(r"\texttt{Input-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        # text_hl = Tex(r"\texttt{Hidden-Layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        # text_output = Tex(r"\texttt{Output-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        # text_hl_2 = Tex(r"(", r"100", r" \ \texttt{Neuronen})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        text_input = Tex(r"\texttt{Input layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        text_hl = Tex(r"\texttt{Hidden layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        text_output = Tex(r"\texttt{Output layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        text_hl_2 = Tex(r"(", r"100", r" \ \texttt{neurons})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        d1 = config["frame_height"]/2 - text_input.get_bottom()[1]

        input_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(9)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        input_layer_2 = input_layer_1.copy()

        dots = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.4)

        input_layer = VGroup(
            input_layer_1, dots, input_layer_2
        ).arrange(DOWN, buff=0.4).set_x(-config["frame_width"]/4 - d_buffer).set_y(-d1/2)

        hidden_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(7)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        dots_2 = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.2)
        
        hidden_layer = VGroup(
            hidden_layer_1, dots_2, hidden_layer_1.copy()
        ).arrange(DOWN, buff=0.2).set_y(-d1/2)

        output_layer = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(10)]
        ).arrange(DOWN, buff=0.2).scale(0.13).set_x(config["frame_width"]/4 + d_buffer).set_y(-d1/2)

        brace_input = Brace(input_layer, LEFT).set_color(BLACK)
        brace_input_text = brace_input.get_tex(r"784").set_color(BLACK)

        brace_hl = Brace(hidden_layer, RIGHT).set_color(BLACK)
        brace_hl_text = brace_hl.get_tex(r"100").set_color(BLACK)

        brace_output = Brace(output_layer, RIGHT).set_color(BLACK)
        brace_output_text = brace_output.get_tex(r"10").set_color(BLACK)

        ####

        # self.add(input_layer, hidden_layer, output_layer, brace_input, brace_input_text, brace_hl, brace_hl_text, brace_output, brace_output_text)
        
        self.play(
            LaggedStart(
                Write(text_input),
                FadeIn(input_layer),
                lag_ratio=0.5
            )
        )
        self.wait(0.5)
        self.play(
            Write(brace_input),
            Write(brace_input_text)
        )
        self.wait()

        self.play(
            LaggedStart(
                Write(text_hl),
                FadeIn(hidden_layer),
                lag_ratio=0.5
            )
        )
        self.wait(0.5)
        self.play(
            Write(brace_hl),
            Write(brace_hl_text)
        )
        self.wait()

        self.play(
            LaggedStart(
                Write(text_output),
                FadeIn(output_layer),
                lag_ratio=0.5
            )
        )
        self.wait(0.5)
        self.play(
            Write(brace_output),
            Write(brace_output_text)
        )
        self.wait()

        ####

        lines = VGroup()
        hidden_layer_neurons = VGroup(*hidden_layer[0], *hidden_layer[-1])

        for j in [0,2]:
            for k in range(9):
                lines_k = VGroup(
                    *[Line(input_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in hidden_layer_neurons]
                )

                lines.add(lines_k)

        lines_2 = VGroup()

        for j in [0,2]:
            for k in range(7):
                lines_k = VGroup(
                    *[Line(hidden_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in output_layer]
                )

                lines_2.add(lines_k)

        self.play(
            Create(lines[0]),
            run_time=4
        )
        self.play(
            Create(lines[1]),
            run_time=2
        )

        self.play(
            LaggedStart(
                *[Create(line) for line in lines[2:]],
                lag_ratio=0.5
            )
        )
        self.wait()

        self.play(
            LaggedStart(
                AnimationGroup(
                    FadeOut(brace_hl),
                    brace_hl_text.animate.scale(0.6).move_to(text_hl_2[1].get_center())
                ),
                FadeIn(text_hl_2[0], text_hl_2[2]),
                lag_ratio=0.5
            )
        )
        
        self.play(
            LaggedStart(
                *[Create(line) for line in lines_2],
                lag_ratio=0.5
            )
        )
        self.wait()


class ConveyerBelt(MovingCameraScene):
    def construct(self):

        self.camera.background_color = WHITE

        d_buffer = 1

        text_input = Tex(r"\texttt{Input-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        text_hl = Tex(r"\texttt{Hidden-Layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        text_output = Tex(r"\texttt{Output-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        text_hl_2 = Tex(r"(", r"100", r" \ \texttt{neurons})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        d1 = config["frame_height"]/2 - text_input.get_bottom()[1]

        input_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(9)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        input_layer_2 = input_layer_1.copy()

        dots = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.4)

        input_layer = VGroup(
            input_layer_1, dots, input_layer_2
        ).arrange(DOWN, buff=0.4).set_x(-config["frame_width"]/4 - d_buffer).set_y(-d1/2)

        hidden_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(7)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        dots_2 = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.2)
        
        hidden_layer = VGroup(
            hidden_layer_1, dots_2, hidden_layer_1.copy()
        ).arrange(DOWN, buff=0.2).set_y(-d1/2)

        output_layer = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(10)]
        ).arrange(DOWN, buff=0.2).scale(0.13).set_x(config["frame_width"]/4 + d_buffer).set_y(-d1/2)

        brace_input = Brace(input_layer, LEFT).set_color(BLACK)
        brace_input_text = brace_input.get_tex(r"784").set_color(BLACK)

        brace_output = Brace(output_layer, RIGHT).set_color(BLACK)
        brace_output_text = brace_output.get_tex(r"10").set_color(BLACK)

        lines = VGroup()
        hidden_layer_neurons = VGroup(*hidden_layer[0], *hidden_layer[-1])

        for j in [0,2]:
            for k in range(9):
                lines_k = VGroup(
                    *[Line(input_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in hidden_layer_neurons]
                )

                lines.add(lines_k)

        lines_2 = VGroup()

        for j in [0,2]:
            for k in range(7):
                lines_k = VGroup(
                    *[Line(hidden_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in output_layer]
                )

                lines_2.add(lines_k)

        self.add(
            input_layer, hidden_layer, output_layer, text_input, text_hl, text_hl_2, text_output, brace_input, brace_input_text, brace_output, brace_output_text, lines, lines_2
        )
        self.wait()

        self.play(
            self.camera.frame.animate.scale(0.2).move_to(input_layer[0][0])
        )
        self.wait()

        self.play(
            VGroup(
                input_layer[1], hidden_layer[1], output_layer, text_input, text_hl, text_hl_2, text_output, brace_input, brace_input_text, brace_output, brace_output_text, lines, lines_2
            ).animate.set_opacity(0.2),
            VGroup(
                input_layer[0], input_layer[-1], hidden_layer[0], hidden_layer[-1]
            ).animate.set_style(stroke_opacity=0.2),
            input_layer[0][0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),

        )
        self.wait()

        input_number = MathTex("x^{(1)}_1").set_color(BLACK).scale(0.2).move_to(input_layer[0][0].get_center()) # .add_background_rectangle(color=WHITE)
        weight_number = MathTex(r" \cdot", "w_1").set_color(BLACK).scale(0.2).move_to(lines[0][0].get_center())

        eq_1 = MathTex("x^{(1)}_1 ", r"\cdot", "w^{(1)}_1").set_color(BLACK).scale(0.2).next_to(lines[0][0].get_center(), UP, buff=0.1).add_background_rectangle(color=WHITE)
        br = BackgroundRectangle(eq_1, color=WHITE)

        self.play(
            FadeIn(input_number)
        )
        self.wait()

        self.play(
            lines[0][0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            )
        )
        self.wait()


        def update_curve(mob):
            mob.move_to(input_number.get_center())

        self.camera.frame.add_updater(update_curve)

        self.play(
            input_number.animate.move_to(eq_1[1].get_center())
        )

        self.camera.frame.remove_updater(update_curve)

        # self.play(
        #     self.camera.frame.animate.move_to(eq_1.get_center()),
        #     run_time=0.5
        # )

        self.play(
            # FadeIn(br),
            FadeIn(eq_1),
            self.camera.frame.animate.move_to(eq_1.get_center()),
        )
        self.remove(input_number)

        self.wait()

        def update_curve_2(mob):
            mob.move_to(eq_1.get_center())
        self.camera.frame.add_updater(update_curve_2)


        self.play(
            eq_1.animate.next_to(
                hidden_layer[0][0], UP, buff=0.07
            ),
            hidden_layer[0][0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),
        )
        self.wait()

        eq_2 = MathTex(r"+ \dots + ", r"x_{784}^{(1)} \cdot w_{784}^{(1)}").set_color(BLACK).scale(0.2).next_to(eq_1, RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
        eq_3 = MathTex(r"+ b_1").set_color(BLACK).scale(0.2).next_to(eq_2, RIGHT, buff=0.03).add_background_rectangle(color=WHITE)

        eq_4 = MathTex(r"x^{(2)}_1", "=").set_color(BLACK).scale(0.2).next_to(eq_1, LEFT, buff=0.03).add_background_rectangle(color=WHITE)

        first_lines = VGroup(
            *[lines[k][0] for k in range(18)]
        )

        self.play(
            ReplacementTransform(
                first_lines[1:].copy(),
                eq_2
            )
        )
        self.wait()

        self.play(
            ReplacementTransform(
                hidden_layer[0][0].copy(),
                eq_3
            )
        )
        self.wait()

        self.play(
            FadeIn(eq_4)
        )
        self.wait()

        hidden_number = eq_4[1].copy()

        self.play(
            hidden_number.animate.move_to(hidden_layer[0][0].get_center())
        )
        self.wait()


class ConveyerBeltVariables_ger(MovingCameraScene):
    def construct(self):

        self.camera.background_color = WHITE

        d_buffer = 1

        # text_input = Tex(r"\texttt{Input-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        # text_hl = Tex(r"\texttt{Hidden-Layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        # text_output = Tex(r"\texttt{Output-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        # text_hl_2 = Tex(r"(", r"100", r" \ \texttt{neurons})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        text_input = Tex(r"\texttt{Input-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        text_hl = Tex(r"\texttt{Hidden-Layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        text_output = Tex(r"\texttt{Output-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        text_hl_2 = Tex(r"(", r"100", r" \ \texttt{Neuronen})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        d1 = config["frame_height"]/2 - text_input.get_bottom()[1]

        input_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(9)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        input_layer_2 = input_layer_1.copy()

        dots = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.4)

        input_layer = VGroup(
            input_layer_1, dots, input_layer_2
        ).arrange(DOWN, buff=0.4).set_x(-config["frame_width"]/4 - d_buffer).set_y(-d1/2)

        hidden_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(7)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        dots_2 = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.2)
        
        hidden_layer = VGroup(
            hidden_layer_1, dots_2, hidden_layer_1.copy()
        ).arrange(DOWN, buff=0.2).set_y(-d1/2)

        output_layer = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(10)]
        ).arrange(DOWN, buff=0.2).scale(0.13).set_x(config["frame_width"]/4 + d_buffer).set_y(-d1/2)

        brace_input = Brace(input_layer, LEFT).set_color(BLACK)
        brace_input_text = brace_input.get_tex(r"784").set_color(BLACK)

        brace_output = Brace(output_layer, RIGHT).set_color(BLACK)
        brace_output_text = brace_output.get_tex(r"10").set_color(BLACK)

        lines = VGroup()
        hidden_layer_neurons = VGroup(*hidden_layer[0], *hidden_layer[-1])

        for j in [0,2]:
            for k in range(9):
                lines_k = VGroup(
                    *[Line(input_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in hidden_layer_neurons]
                )

                lines.add(lines_k)

        lines_2 = VGroup()

        for j in [0,2]:
            for k in range(7):
                lines_k = VGroup(
                    *[Line(hidden_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in output_layer]
                )

                lines_2.add(lines_k)

        self.add(
            input_layer, hidden_layer, output_layer, text_input, text_hl, text_hl_2, text_output, brace_input, brace_input_text, brace_output, brace_output_text, lines, lines_2
        )
        self.wait()

        self.play(
            self.camera.frame.animate.scale(0.4).move_to(input_layer[0].get_center()+2.3*RIGHT)
        )
        self.wait()

        self.play(
            VGroup(
                input_layer[1], hidden_layer[1], text_input, text_hl, text_hl_2, text_output, brace_input, brace_input_text, brace_output, brace_output_text, lines, lines_2
            ).animate.set_opacity(0.2),
            VGroup(
                input_layer[0], input_layer[-1], hidden_layer[0], hidden_layer[-1], output_layer,
            ).animate.set_style(stroke_opacity=0.2),
            input_layer[0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),
            input_layer[-1].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),

        )
        self.wait()

        input_numbers = VGroup(
            *[
                MathTex(
                    "a^{(0)}"+"_{}".format(k),
                    color=BLACK
                ).scale(0.25).move_to(input_layer[0][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(9)
            ]
        )

        self.play(
            FadeIn(input_numbers)
        )
        self.wait()

        first_lines = VGroup(
            *[lines[k][0] for k in range(18)]
        )

        self.play(
            lines.animate.set_opacity(0.1),
        )
        self.play(
            hidden_layer[0][0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),
            first_lines.animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            )
        )
        self.wait()

        self.play(
            *[
                input_numbers[k].animate.move_to(first_lines[k].point_from_proportion(0.175))
                for k in range(9)
            ]
        )
        self.wait()

        m_dots = VGroup(
            *[
                
                Dot(
                    color=BLACK
                ).scale(0.12).next_to(input_numbers[k], RIGHT, buff=0.03).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        weight_equations = VGroup(
            *[
                MathTex(
                    "w^{(0)}"+"_{}".format(k),
                    color=RED_E,
                ).scale(0.25).next_to(m_dots[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )


        self.play(
            FadeIn(m_dots),
            FadeIn(weight_equations)
        )
        self.wait()

        text_weights = Tex(r"\texttt{Gewichte}").scale(0.4).set_color(RED_E).next_to(weight_equations, UP, buff=0.15)

        self.play(
            LaggedStart(
                FadeIn(text_weights),
                Circumscribe(weight_equations, color=RED_E, buff=0.02, time_width=2, run_time=3, stroke_width=2),
                lag_ratio=0.5
            )
        )
        self.wait()

        middle_numbers = VGroup(
            *[
                VGroup(
                    input_numbers[k],
                    m_dots[k],
                    weight_equations[k]
                )
                for k in range(9)
            ]
        )

        middle_numbers_2 = VGroup(
            *[
                VGroup(
                    MathTex(
                        "a^{(0)}" + "_{" + "{}".format(k+775) + "}",
                        color=BLACK
                    ).scale(0.25),
                    Dot(
                        color=BLACK
                    ).scale(0.12),
                    MathTex(
                        "w^{(0)}" + "_{" + "{}".format(k+775) + "}",
                        color=RED_E,
                    ).scale(0.25)
                ).arrange(RIGHT, buff=0.03).move_to(first_lines[k+9].point_from_proportion(0.3)).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(9)
            ]
        )

        self.add(middle_numbers_2)


        self.play(
            FadeOut(
                text_weights
            )
        )
        self.play(
            *[
                middle_numbers[k].animate.move_to(first_lines[k].point_from_proportion(0.99)).scale(0.5)
                for k in range(9)
            ],
            *[
                middle_numbers_2[k].animate.move_to(first_lines[k+9].point_from_proportion(0.99)).scale(0.5)
                for k in range(9)
            ],
            self.camera.frame.animate.set_x(2),
            run_time=2
        )

        dots_eq = VGroup(
            *[Dot(color=BLACK).scale(0.075) for _ in range(3)]
        ).arrange(RIGHT, buff=0.04).move_to(hidden_layer[0][0].get_left())


        self.remove(
            middle_numbers[3]
        )
        self.remove(
            middle_numbers[4]
        )
        self.remove(
            middle_numbers[5]
        )
        self.remove(
            middle_numbers[6]
        )
        self.remove(
            middle_numbers[7]
        )
        self.remove(
            middle_numbers[8]
        )
        self.remove(
            middle_numbers_2[0]
        )
        self.remove(
            middle_numbers_2[1]
        )
        self.remove(
            middle_numbers_2[2]
        )
        self.remove(
            middle_numbers_2[3]
        )
        self.remove(
            middle_numbers_2[4]
        )
        self.remove(
            middle_numbers_2[5]
        )

        sum_group = VGroup(
            *[middle_numbers[k] for k in range(3)],
            dots_eq,
            *[middle_numbers_2[k] for k in range(6,9)]
        )

        sum_group_aux = sum_group.copy()
        sum_group_aux.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.3*UP + 2*RIGHT)
        pluses = VGroup(
            *[
                MathTex("+").set_color(BLACK).scale(0.3).move_to(
                    sum_group_aux[k].get_right() + 0.5 * (sum_group_aux[k+1].get_left() - sum_group_aux[k].get_right())
                )
                for k in range(6)
            ]
        )


        self.play(
            sum_group.animate.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.3*UP + 2*RIGHT), #.align_to(hidden_layer[0][0], 2*UP+2*LEFT)
            # sum_group[5].animate.set_color(BLACK),
            FadeIn(pluses) 
        )

        brace_sum = Brace(sum_group, UP, stroke_width=0.2, buff=0.03).set_color(BLACK).stretch_to_fit_height(0.1)
        brace_sum_text = brace_sum.get_tex(r"784 \ \texttt{Summanden}").set_color(BLACK).scale(0.4).next_to(brace_sum, UP, buff=0.1)

        self.play(
            FadeIn(
                brace_sum, brace_sum_text
            )
        )

        self.wait()

        bias_num = MathTex(
            "+", "b^{(1)}_0",
            color=RED_E
        ).scale(0.25).next_to(sum_group_aux, RIGHT, buff=0.05)

        self.play(
            ReplacementTransform(
                hidden_layer[0][0].copy(),
                bias_num
            )
        )

        text_bias = Tex(r"\texttt{Bias}").scale(0.4).set_color(RED_E).next_to(bias_num[1], UP, buff=0.15)

        self.play(
            FadeIn(text_bias)
        )

        self.wait()

        bra_left = MathTex("(").set_color(DARK_BROWN).scale(0.5).next_to(sum_group_aux, LEFT, buff=0.03)
        bra_right = MathTex(")").set_color(DARK_BROWN).scale(0.5).next_to(bias_num, RIGHT, buff=0.03)

        text_func = MathTex(r"\varphi_{0}^{(1)}").scale(0.3).set_color(DARK_BROWN).next_to(bra_left, LEFT, buff=0.05) ######################### HERE

        self.play(
            FadeIn(
                bra_left, bra_right, text_func
            )
        )
        self.wait()

        hidden_input_num = MathTex(
            "=", "a^{(1)}_0",
        ).set_color(BLACK).scale(0.25).next_to(sum_group[4], DOWN, buff=0.15)

        self.play(
            FadeIn(hidden_input_num)
        )
        self.wait()

        hidden_layer_inputs_1 = VGroup(
            *[
                MathTex(
                    "a^{(1)}"+"_{}".format(k),
                    color=BLACK,
                ).scale(0.25).move_to(hidden_layer[0][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )
        hidden_layer_inputs_2 = VGroup(
            *[
                MathTex(
                    "a^{(1)}" + "_{" + "{}".format(k+93) + "}",
                    color=BLACK,
                ).scale(0.25).move_to(hidden_layer[-1][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )

        self.play(
            #hidden_input_num[1].copy().animate.scale(0.8).move_to(hidden_layer[0][0].get_center())
            ReplacementTransform(
                hidden_input_num[1].copy(),
                hidden_layer_inputs_1[0]
            )
        )
        self.wait()


        self.play(
            LaggedStart(
                FadeOut(
                    sum_group, hidden_input_num, text_func, text_bias, pluses, bra_left, bra_right, bias_num, brace_sum, brace_sum_text
                ),
                self.camera.frame.animate.scale(2.25).move_to(hidden_layer.get_center()),
                lag_ratio=0.5
            )
        )
        self.wait()

        lines_aux = lines.copy()
        lines_aux.set_color(GREEN_E).set_opacity(1)

        solo_lines = VGroup()

        for group in lines_aux:
            for line in group:
                solo_lines.add(line)

        self.play(
            *[
                Create(line) for line in solo_lines
            ]
        )

        for line in solo_lines:
            line.reverse_points()

        first_lines.set_color(BLACK).set_opacity(0.1)

        self.play(
            *[
                Uncreate(line) for line in solo_lines
            ],
            VGroup(
                hidden_layer[0], hidden_layer[-1],
            ).animate.set_style(stroke_color=GREEN_E, stroke_opacity=1),
            VGroup(
                input_layer[0], input_layer[-1],
            ).animate.set_style(stroke_color=BLACK, stroke_opacity=0.2),
            FadeIn(
                hidden_layer_inputs_1[1:], hidden_layer_inputs_2
            )
            # rate_func = lambda t: smooth(t)
        )
        self.wait(2)

        first_lines_2 = VGroup(
            *[lines_2[k][0] for k in range(14)]
        )

        self.play(
            self.camera.frame.animate.scale(0.4).shift(RIGHT*2.25).set_y(hidden_layer[0].get_y()),
            lines_2.animate.set_opacity(0.1)
        )
        self.play(
            first_lines_2.animate.set_opacity(1).set_color(GREEN_E),
            output_layer[0].animate.set_stroke(color=GREEN_E, opacity=1),
        )
        self.wait()

        ################################################################################################################################


        self.play(
            *[
                hidden_layer_inputs_1[k].animate.move_to(first_lines_2[k].point_from_proportion(0.175))
                for k in range(7)
            ]
        )
        self.wait()

        m_dots_2 = VGroup(
            *[
                Dot(
                    color=BLACK
                ).scale(0.12).next_to(hidden_layer_inputs_1[k], RIGHT, buff=0.03).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        weight_equations_2 = VGroup(
            *[
                MathTex(
                    "w^{(1)}"+"_{}".format(k),
                    color=RED_E,
                ).scale(0.25).next_to(m_dots_2[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )


        self.play(
            FadeIn(m_dots_2),
            FadeIn(weight_equations_2)
        )
        self.wait()

        text_weights_2 = Tex(r"\texttt{Gewichte}").scale(0.4).set_color(RED_E).next_to(weight_equations_2, UP, buff=0.15)

        self.play(
            LaggedStart(
                FadeIn(text_weights_2),
                Circumscribe(weight_equations_2, color=RED_E, buff=0.02, time_width=2, run_time=3, stroke_width=2),
                lag_ratio=0.5
            )
        )
        self.wait()


        # middle_numbers_2 = VGroup(
        #     *[
        #         DecimalNumber(
        #             hidden_layer_inputs_vals[k]*weight_values_2[k],
        #             num_decimal_places=1,
        #             color=BLACK
        #         ).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE)
        #         for k in range(7)
        #     ]
        # )


        # middle_numbers_2_2 = VGroup(
        #     *[
        #         DecimalNumber(
        #             middle_numbers_2_2_vals[k],
        #             num_decimal_places=1,
        #             color=BLACK
        #         ).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE).move_to(first_lines_2[k+7].point_from_proportion(0.175))
        #         for k in range(7)
        #     ]
        # )
        # self.add(middle_numbers_2_2)

        middle_numbers_2 = VGroup(
            *[
                VGroup(
                    hidden_layer_inputs_1[k],
                    m_dots_2[k],
                    weight_equations_2[k]
                )
                for k in range(7)
            ]
        )

        middle_numbers_2_2 = VGroup(
            *[
                VGroup(
                    MathTex(
                        "a^{(1)}" + "_{" + "{}".format(k+93) + "}",
                        color=BLACK
                    ).scale(0.25),
                    Dot(
                        color=BLACK
                    ).scale(0.12),
                    MathTex(
                        "w^{(1)}" + "_{" + "{}".format(k+93) + "}",
                        color=RED_E,
                    ).scale(0.25)
                ).arrange(RIGHT, buff=0.03).move_to(first_lines_2[k+7].point_from_proportion(0.3)).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )
        self.add(middle_numbers_2_2)


        self.play(
            FadeOut(
                text_weights_2
            )
        )
        self.play(
            *[
                middle_numbers_2[k].animate.move_to(first_lines_2[k].point_from_proportion(0.99)).scale(0.2)
                for k in range(7)
            ],
            *[
                middle_numbers_2_2[k].animate.move_to(first_lines_2[k+7].point_from_proportion(0.99)).scale(0.2)
                for k in range(7)
            ],
            run_time=1
        )
        #self.wait()

        dots_eq_2 = VGroup(
            *[Dot(color=BLACK).scale(0.03) for _ in range(3)]
        ).arrange(RIGHT, buff=0.01).move_to(output_layer[0].get_left())

        self.remove(
            middle_numbers_2[2]
        )
        self.remove(
            middle_numbers_2[3]
        )
        self.remove(
            middle_numbers_2[4]
        )
        self.remove(
            middle_numbers_2[5]
        )
        self.remove(
            middle_numbers_2[6]
        )
        self.remove(
            middle_numbers_2_2[0]
        )
        self.remove(
            middle_numbers_2_2[1]
        )
        self.remove(
            middle_numbers_2_2[2]
        )
        self.remove(
            middle_numbers_2_2[3]
        )
        self.remove(
            middle_numbers_2_2[4]
        )


        sum_group_2 = VGroup(
            *[middle_numbers_2[k] for k in range(2)],
            dots_eq_2,
            *[middle_numbers_2_2[k] for k in range(5,7)]
        )

        sum_group_aux_2 = sum_group_2.copy()
        sum_group_aux_2.scale(7).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.1*UP + 2.4*RIGHT)
        pluses_2 = VGroup(
            *[
                MathTex("+").set_color(BLACK).scale(0.3).move_to(
                    sum_group_aux_2[k].get_right() + 0.5 * (sum_group_aux_2[k+1].get_left() - sum_group_aux_2[k].get_right())
                )
                for k in range(4)
            ]
        )

        self.play(
            sum_group_2.animate.scale(7).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.1*UP + 2.4*RIGHT), #.align_to(hidden_layer[0][0], 2*UP+2*LEFT)
            # sum_group[5].animate.set_color(BLACK),
            FadeIn(pluses_2) 
        )

        brace_sum_2 = Brace(sum_group_2, UP, stroke_width=0.2, buff=0).set_color(BLACK).stretch_to_fit_height(0.1).shift(DOWN*0.05)
        brace_sum_text_2 = brace_sum_2.get_tex(r"100 \ \texttt{Summanden}").set_color(BLACK).scale(0.4).next_to(brace_sum_2, UP, buff=0.1)

        self.play(
            FadeIn(
                brace_sum_2, brace_sum_text_2
            )
        )

        self.wait()

        bias_num_2 = MathTex(
            "+", "b^{(2)}_0",
            color=RED_E
        ).scale(0.35).next_to(sum_group_aux_2, RIGHT, buff=0.05)

        self.play(
            ReplacementTransform(
                output_layer[0][0].copy(),
                bias_num_2
            )
        )

        text_bias_2 = Tex(r"\texttt{Bias}").scale(0.4).set_color(RED_E).next_to(bias_num_2[1], UP, buff=0.15)

        self.play(
            FadeIn(text_bias_2),
            FadeOut(hidden_layer_inputs_2)
        )

        self.wait()

        bra_left_2 = MathTex("(").set_color(DARK_BROWN).scale(0.5).next_to(sum_group_aux_2, LEFT, buff=0.05)
        bra_right_2 = MathTex(")").set_color(DARK_BROWN).scale(0.5).next_to(bias_num_2, RIGHT, buff=0.03)

        text_func_2 = MathTex(r"\varphi^{(2)}").scale(0.4).set_color(DARK_BROWN).next_to(bra_left_2, LEFT, buff=0.05)

        self.play(
            FadeIn(
                bra_left_2, bra_right_2, text_func_2
            )
        )
        self.wait()

        hidden_input_num_2 = MathTex(
            "=", "a^{(2)}_0",
        ).set_color(BLACK).scale(0.45).next_to(sum_group_2[4], DOWN, buff=0.25)

        self.play(
            FadeIn(hidden_input_num_2)
        )
        self.wait()

        self.play(
            hidden_input_num_2[1].copy().animate.scale(0.6).move_to(output_layer[0].get_center())
        )
        self.wait()

        self.play(
            LaggedStart(
                FadeOut(
                    sum_group_2, hidden_input_num_2, text_func_2, text_bias_2, pluses_2, bra_left_2, bra_right_2, bias_num_2, brace_sum_2, brace_sum_text_2
                ),
                self.camera.frame.animate.scale(2.25).move_to(hidden_layer.get_center()),
                lag_ratio=0.5
            )
        )
        self.wait()

        lines_aux_2 = lines_2.copy()
        lines_aux_2.set_color(GREEN_E).set_opacity(1)

        solo_lines_2 = VGroup()

        for group in lines_aux_2:
            for line in group:
                solo_lines_2.add(line)

        self.play(
            *[
                Create(line) for line in solo_lines_2
            ]
        )

        for line in solo_lines_2:
            line.reverse_points()

        first_lines_2.set_color(BLACK).set_opacity(0.1)

        output_layer_numbers = VGroup(
            *[
                MathTex(
                    "a^{(2)}_{" + "{}".format(k+1) + "}",
                    color=BLACK,
                ).scale(0.25).move_to(output_layer[k+1].get_center())
                for k in range(9)
            ]
        )

        self.play(
            *[
                Uncreate(line) for line in solo_lines_2
            ],
            output_layer.animate.set_style(stroke_color=GREEN_E, stroke_opacity=1),
            VGroup(
                hidden_layer[0], hidden_layer[-1],
            ).animate.set_style(stroke_color=BLACK, stroke_opacity=0.2),
            FadeIn(
                output_layer_numbers
            )
            # rate_func = lambda t: smooth(t)
        )
        self.wait()


class ConveyerBeltNumbers_eng(MovingCameraScene):
    def construct(self):

        self.camera.background_color = WHITE

        d_buffer = 1

        # text_input = Tex(r"\texttt{Input-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        # text_hl = Tex(r"\texttt{Hidden-Layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        # text_output = Tex(r"\texttt{Output-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        # text_hl_2 = Tex(r"(", r"100", r" \ \texttt{Neuronen})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        text_input = Tex(r"\texttt{Input layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        text_hl = Tex(r"\texttt{Hidden layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        text_output = Tex(r"\texttt{Output layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        text_hl_2 = Tex(r"(", r"100", r" \ \texttt{neurons})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        d1 = config["frame_height"]/2 - text_input.get_bottom()[1]

        input_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(9)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        input_layer_2 = input_layer_1.copy()

        dots = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.4)

        input_layer = VGroup(
            input_layer_1, dots, input_layer_2
        ).arrange(DOWN, buff=0.4).set_x(-config["frame_width"]/4 - d_buffer).set_y(-d1/2)

        hidden_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(7)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        dots_2 = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.2)
        
        hidden_layer = VGroup(
            hidden_layer_1, dots_2, hidden_layer_1.copy()
        ).arrange(DOWN, buff=0.2).set_y(-d1/2)

        output_layer = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(10)]
        ).arrange(DOWN, buff=0.2).scale(0.13).set_x(config["frame_width"]/4 + d_buffer).set_y(-d1/2)

        brace_input = Brace(input_layer, LEFT).set_color(BLACK)
        brace_input_text = brace_input.get_tex(r"784").set_color(BLACK)

        brace_output = Brace(output_layer, RIGHT).set_color(BLACK)
        brace_output_text = brace_output.get_tex(r"10").set_color(BLACK)

        lines = VGroup()
        hidden_layer_neurons = VGroup(*hidden_layer[0], *hidden_layer[-1])

        for j in [0,2]:
            for k in range(9):
                lines_k = VGroup(
                    *[Line(input_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in hidden_layer_neurons]
                )

                lines.add(lines_k)

        lines_2 = VGroup()

        for j in [0,2]:
            for k in range(7):
                lines_k = VGroup(
                    *[Line(hidden_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in output_layer]
                )

                lines_2.add(lines_k)

        self.add(
            input_layer, hidden_layer, output_layer, text_input, text_hl, text_hl_2, text_output, brace_input, brace_input_text, brace_output, brace_output_text, lines, lines_2
        )
        self.wait()

        self.play(
            self.camera.frame.animate.scale(0.4).move_to(input_layer[0].get_center()+2.3*RIGHT)
        )
        self.wait()

        self.play(
            VGroup(
                input_layer[1], hidden_layer[1], text_input, text_hl, text_hl_2, text_output, brace_input, brace_input_text, brace_output, brace_output_text, lines, lines_2
            ).animate.set_opacity(0.2),
            VGroup(
                input_layer[0], input_layer[-1], hidden_layer[0], hidden_layer[-1], output_layer,
            ).animate.set_style(stroke_opacity=0.2),
            input_layer[0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),
            input_layer[-1].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),

        )
        self.wait()

        input_values = [
            0.0, 0.0, 0.1, 0.2, 0.2, 0.7, 1.0, 0.7, 0.2
        ]

        weight_values = [
            2.0, -3.0, 2.5, 8.0, -2.5, -2.0, 5.0, 7.0, -0.5
        ]

        input_numbers = VGroup(
            *[
                DecimalNumber(
                    input_values[k],
                    num_decimal_places=1,
                    color=BLACK
                ).scale(0.3).move_to(input_layer[0][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(9)
            ]
        )

        self.play(
            FadeIn(input_numbers)
        )
        self.wait()

        first_lines = VGroup(
            *[lines[k][0] for k in range(18)]
        )

        self.play(
            lines.animate.set_opacity(0.1),
        )
        self.play(
            hidden_layer[0][0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),
            first_lines.animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            )
        )
        self.wait()

        self.play(
            *[
                input_numbers[k].animate.move_to(first_lines[k].point_from_proportion(0.175))
                for k in range(9)
            ]
        )
        self.wait()

        x_aux_1 = VGroup(
            Dot(color=BLACK).scale(0.12),
            MathTex(
                "(-2.5)",
                color=RED_E,
            ).scale(0.3),
        ).arrange(RIGHT, buff=0.03).next_to(input_numbers[0], RIGHT, buff=0.03).get_x()

        m_dots = VGroup(
            *[
                
                Dot(
                    color=BLACK
                ).scale(0.12).next_to(input_numbers[k], RIGHT, buff=0.03).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        weight_equations = VGroup(
            *[
                VGroup(
                    # Dot(color=BLACK).scale(0.12),
                    # DecimalNumber(
                    #     weight_values[k],
                    #     num_decimal_places=1,
                    #     color=RED_E
                    # ).scale(0.3) 
                    MathTex(
                        "{}".format(weight_values[k]),
                        color=RED_E,
                    ).scale(0.3) if weight_values[k]>0 else
                    MathTex(
                        "({})".format(weight_values[k]),
                        color=RED_E,
                    ).scale(0.3),
                ).arrange(RIGHT, buff=0.03).next_to(m_dots[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        # x_aux_decimal_point = weight_equations[5][2].get_x()

        # x_aux_decimal_point = weight_equations[1][0][3].get_x()

        shift_vals = [
            0.17, 0, 0.17, 0.17, 0, 0, 0.17, 0.17, 0
        ]

        for k in range(9):
            weight_equations[k].shift(RIGHT*shift_vals[k])

        # for k in range(9):
        #     x_aux = weight_equations[k][1].get_x()
        #     shift_val = x_aux - x_aux_decimal_point
        #     weight_equations[k][2].shift( RIGHT )

        self.play(
            FadeIn(m_dots),
            FadeIn(weight_equations)
        )
        self.wait()

        text_weights = Tex(r"\texttt{Weights}").scale(0.4).set_color(RED_E).next_to(weight_equations, UP, buff=0.15)

        self.play(
            LaggedStart(
                FadeIn(text_weights),
                Circumscribe(weight_equations, color=RED_E, buff=0.02, time_width=2, run_time=3, stroke_width=2),
                lag_ratio=0.5
            )
        )
        self.wait()

        middle_numbers = VGroup(
            *[
                DecimalNumber(
                    input_values[k]*weight_values[k],
                    num_decimal_places=1,
                    color=BLACK
                ).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        middle_numbers_2_vals = [
            -4.2, 3, 12.2, 0.7, -0.2, -2.2, 9.6, 0.0, 0.0
        ]

        middle_numbers_2 = VGroup(
            *[
                DecimalNumber(
                    middle_numbers_2_vals[k],
                    num_decimal_places=1,
                    color=BLACK
                ).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE).move_to(first_lines[k+9].point_from_proportion(0.3))
                for k in range(9)
            ]
        )
        self.add(middle_numbers_2)

        equals_group = VGroup(
            *[
                MathTex("=").set_color(BLACK).scale(0.3).next_to(weight_equations[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        x_equal_aux = equals_group[-1].get_x()

        for sign in equals_group:
            sign.set_x(x_equal_aux)

        weight_solutions = VGroup(
            *[
                middle_numbers[k].next_to(equals_group[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        x_dp_aux = middle_numbers[4][3].get_x()

        dp_placement = [
            2, 2, 2, 2, 3, 3, 2, 2, 3
        ]

        for k in range(9):
            x_diff = middle_numbers[k][dp_placement[k]].get_x() - x_dp_aux
            weight_solutions[k].shift(LEFT*x_diff)

        self.play(
            FadeIn(equals_group),
            FadeIn(weight_solutions)
        )
        self.wait()

        self.play(
            FadeOut(
                text_weights, input_numbers, weight_equations, m_dots, equals_group, *[weight_solutions[k][:2] for k in range(9)]
            )
        )
        self.play(
            *[
                middle_numbers[k].animate.move_to(first_lines[k].point_from_proportion(0.99)).scale(0.5)
                for k in range(9)
            ],
            *[
                middle_numbers_2[k].animate.move_to(first_lines[k+9].point_from_proportion(0.99)).scale(0.5)
                for k in range(9)
            ],
            self.camera.frame.animate.set_x(2),
            run_time=2
        )

        dots_eq = VGroup(
            *[Dot(color=BLACK).scale(0.075) for _ in range(3)]
        ).arrange(RIGHT, buff=0.04).move_to(hidden_layer[0][0].get_left())

        for num in middle_numbers:
            if num.get_value()<0:
                val = num.get_value()
                num.become(
                    MathTex("( {} )".format(val)).set_color(BLACK).scale(0.3).scale(0.5),
                    match_center=True,
                )
        
        for num in middle_numbers_2:
            if num.get_value()<0:
                val = num.get_value()
                num.become(
                    MathTex("( {} )".format(val)).set_color(BLACK).scale(0.3).scale(0.5),
                    match_center=True,
                )

        self.remove(
            middle_numbers[5]
        )
        self.remove(
            middle_numbers[6]
        )
        self.remove(
            middle_numbers[7]
        )
        self.remove(
            middle_numbers[8]
        )
        self.remove(
            middle_numbers_2[0]
        )
        self.remove(
            middle_numbers_2[1]
        )
        self.remove(
            middle_numbers_2[2]
        )
        self.remove(
            middle_numbers_2[3]
        )

        sum_group = VGroup(
            *[middle_numbers[k] for k in range(5)],
            dots_eq,
            *[middle_numbers_2[k] for k in range(4,9)]
        )

        sum_group_aux = sum_group.copy()
        sum_group_aux.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.3*UP + 2.5*RIGHT)
        pluses = VGroup(
            *[
                MathTex("+").set_color(BLACK).scale(0.3).move_to(
                    sum_group_aux[k].get_right() + 0.5 * (sum_group_aux[k+1].get_left() - sum_group_aux[k].get_right())
                )
                for k in range(10)
            ]
        )


        self.play(
            sum_group.animate.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.3*UP + 2.5*RIGHT), #.align_to(hidden_layer[0][0], 2*UP+2*LEFT)
            # sum_group[5].animate.set_color(BLACK),
            FadeIn(pluses) 
        )

        brace_sum = Brace(sum_group, UP, stroke_width=0.2, buff=0.03).set_color(BLACK).stretch_to_fit_height(0.1)
        brace_sum_text = brace_sum.get_tex(r"784 \ \texttt{summands}").set_color(BLACK).scale(0.4).next_to(brace_sum, UP, buff=0.1)

        self.play(
            FadeIn(
                brace_sum, brace_sum_text
            )
        )

        self.wait()

        bias_num = MathTex(
            "1.7", "+",
            color=RED_E
        ).scale(0.3).next_to(sum_group_aux, LEFT, buff=0.05)

        self.play(
            ReplacementTransform(
                hidden_layer[0][0].copy(),
                bias_num
            )
        )

        text_bias = Tex(r"\texttt{Bias}").scale(0.4).set_color(RED_E).next_to(bias_num[0], UP, buff=0.15)

        self.play(
            FadeIn(text_bias)
        )

        self.wait()

        bra_left = MathTex("[").set_color(DARK_BROWN).scale(0.4).next_to(bias_num, LEFT, buff=0.05)
        bra_right = MathTex("]").set_color(DARK_BROWN).scale(0.4).next_to(sum_group_aux, RIGHT, buff=0.05)

        text_func = Tex(r"\texttt{ReLU}").scale(0.4).set_color(DARK_BROWN).next_to(bra_left, LEFT, buff=0.05)

        self.play(
            FadeIn(
                bra_left, bra_right, text_func
            )
        )
        self.wait()

        hidden_input_num = MathTex(
            "=", "8.7",
        ).set_color(BLACK).scale(0.3).next_to(sum_group[4], DOWN, buff=0.15)

        self.play(
            FadeIn(hidden_input_num)
        )
        self.wait()

        hidden_layer_inputs_vals = [
            8.7, 5.3, 0.0, 0.0, 1.4, 1.2, 4.9, 2.2, 0.0, 9.4, 7.8, 0.0, 6.0, 0.0
        ]

        hidden_layer_inputs_1 = VGroup(
            *[
                DecimalNumber(
                    hidden_layer_inputs_vals[k],
                    color=BLACK,
                    num_decimal_places=1
                ).scale(0.3).move_to(hidden_layer[0][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )
        hidden_layer_inputs_2 = VGroup(
            *[
                DecimalNumber(
                    hidden_layer_inputs_vals[k+7],
                    color=BLACK,
                    num_decimal_places=1
                ).scale(0.3).move_to(hidden_layer[-1][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )

        self.play(
            #hidden_input_num[1].copy().animate.scale(0.8).move_to(hidden_layer[0][0].get_center())
            ReplacementTransform(
                hidden_input_num[1].copy(),
                hidden_layer_inputs_1[0]
            )
        )
        self.wait()


        self.play(
            LaggedStart(
                FadeOut(
                    sum_group, hidden_input_num, text_func, text_bias, pluses, bra_left, bra_right, bias_num, brace_sum, brace_sum_text
                ),
                self.camera.frame.animate.scale(2.25).move_to(hidden_layer.get_center()),
                lag_ratio=0.5
            )
        )
        self.wait()

        lines_aux = lines.copy()
        lines_aux.set_color(GREEN_E).set_opacity(1)

        solo_lines = VGroup()

        for group in lines_aux:
            for line in group:
                solo_lines.add(line)

        self.play(
            *[
                Create(line) for line in solo_lines
            ]
        )

        for line in solo_lines:
            line.reverse_points()

        first_lines.set_color(BLACK).set_opacity(0.1)

        self.play(
            *[
                Uncreate(line) for line in solo_lines
            ],
            VGroup(
                hidden_layer[0], hidden_layer[-1],
            ).animate.set_style(stroke_color=GREEN_E, stroke_opacity=1),
            VGroup(
                input_layer[0], input_layer[-1],
            ).animate.set_style(stroke_color=BLACK, stroke_opacity=0.2),
            FadeIn(
                hidden_layer_inputs_1[1:], hidden_layer_inputs_2
            )
            # rate_func = lambda t: smooth(t)
        )
        self.wait(2)

        first_lines_2 = VGroup(
            *[lines_2[k][0] for k in range(14)]
        )

        self.play(
            self.camera.frame.animate.scale(0.4).shift(RIGHT*2.25).set_y(hidden_layer[0].get_y()),
            lines_2.animate.set_opacity(0.1)
        )
        self.play(
            first_lines_2.animate.set_opacity(1).set_color(GREEN_E),
            output_layer[0].animate.set_stroke(color=GREEN_E, opacity=1),
        )
        self.wait()

        ################################################################################################################################

        weight_values_2 = [
            3.0, 7.0, -0.5, 9.0, -1.0, -2.0, -8.0
        ]


        self.play(
            *[
                hidden_layer_inputs_1[k].animate.move_to(first_lines_2[k].point_from_proportion(0.175))
                for k in range(7)
            ]
        )
        self.wait()

        m_dots_2 = VGroup(
            *[
                Dot(
                    color=BLACK
                ).scale(0.12).next_to(hidden_layer_inputs_1[k], RIGHT, buff=0.03).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        weight_equations_2 = VGroup(
            *[
                VGroup(
                    DecimalNumber(
                        weight_values_2[k],
                        num_decimal_places=1,
                        color=RED_E
                    ).scale(0.3) if weight_values_2[k]>0 else
                    MathTex(
                        "({})".format(weight_values_2[k]),
                        color=RED_E,
                    ).scale(0.3),
                ).arrange(RIGHT, buff=0.03).next_to(m_dots_2[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        shift_vals_3 = [
            0.165, 0.165, 0, 0.165, 0, 0, 0,
        ]

        for k in range(7):
            weight_equations_2[k].shift(RIGHT*shift_vals_3[k])

        self.play(
            FadeIn(m_dots_2),
            FadeIn(weight_equations_2)
        )
        self.wait()

        text_weights_2 = Tex(r"\texttt{Weights}").scale(0.4).set_color(RED_E).next_to(weight_equations_2, UP, buff=0.15)

        self.play(
            LaggedStart(
                FadeIn(text_weights_2),
                Circumscribe(weight_equations_2, color=RED_E, buff=0.02, time_width=2, run_time=3, stroke_width=2),
                lag_ratio=0.5
            )
        )
        self.wait()


        middle_numbers_2 = VGroup(
            *[
                DecimalNumber(
                    hidden_layer_inputs_vals[k]*weight_values_2[k],
                    num_decimal_places=1,
                    color=BLACK
                ).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        middle_numbers_2_2_vals = [
            -6.9, 3, 0.0, 0.7, -0.2, 0.0, 3.1
        ]

        middle_numbers_2_2 = VGroup(
            *[
                DecimalNumber(
                    middle_numbers_2_2_vals[k],
                    num_decimal_places=1,
                    color=BLACK
                ).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE).move_to(first_lines_2[k+7].point_from_proportion(0.175))
                for k in range(7)
            ]
        )
        self.add(middle_numbers_2_2)


        equals_group_2 = VGroup(
            *[
                MathTex("=").set_color(BLACK).scale(0.3).next_to(weight_equations_2[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        x_equal_aux_2 = equals_group_2[2].get_x()

        for sign in equals_group_2:
            sign.set_x(x_equal_aux_2)

        weight_solutions_2 = VGroup(
            *[
                middle_numbers_2[k].next_to(equals_group_2[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        x_dp_aux_2 = middle_numbers_2[-1][4].get_x()

        dp_placement = [
            3, 3, 2, 2, 3, 3, 4
        ]

        for k in range(7):
            x_diff = x_dp_aux_2 - middle_numbers_2[k][dp_placement[k]].get_x()
            weight_solutions_2[k].shift(RIGHT*x_diff)


        self.play(
            FadeIn(equals_group_2),
            FadeIn(weight_solutions_2)
        )
        self.wait()


        self.play(
            FadeOut(
                text_weights_2, hidden_layer_inputs_1, hidden_layer_inputs_2, weight_equations_2, m_dots_2, equals_group_2, *[weight_solutions_2[k][:2] for k in range(7)]
            )
        )
        self.play(
            *[
                middle_numbers_2[k].animate.move_to(first_lines_2[k].point_from_proportion(0.99)).scale(0.5)
                for k in range(7)
            ],
            *[
                middle_numbers_2_2[k].animate.move_to(first_lines_2[k+7].point_from_proportion(0.99)).scale(0.5)
                for k in range(7)
            ],
            run_time=1
        )
        #self.wait()

        dots_eq_2 = VGroup(
            *[Dot(color=BLACK).scale(0.075) for _ in range(3)]
        ).arrange(RIGHT, buff=0.04).move_to(output_layer[0].get_left())

        for num in middle_numbers_2:
            if num.get_value()<0:
                val = num.get_value()
                num.become(
                    MathTex("( {} )".format(val)).set_color(BLACK).scale(0.3).scale(0.5),
                    match_center=True,
                )
        
        for num in middle_numbers_2_2:
            if num.get_value()<0:
                val = num.get_value()
                num.become(
                    MathTex("( {} )".format(val)).set_color(BLACK).scale(0.3).scale(0.5),
                    match_center=True,
                )

        self.remove(
            middle_numbers_2[4]
        )
        self.remove(
            middle_numbers_2[5]
        )
        self.remove(
            middle_numbers_2[6]
        )
        self.remove(
            middle_numbers_2_2[0]
        )
        self.remove(
            middle_numbers_2_2[1]
        )
        self.remove(
            middle_numbers_2_2[2]
        )


        sum_group_2 = VGroup(
            *[middle_numbers_2[k] for k in range(4)],
            dots_eq_2,
            *[middle_numbers_2_2[k] for k in range(3,7)]
        )

        sum_group_aux_2 = sum_group_2.copy()
        sum_group_aux_2.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.1*UP + 3*RIGHT)
        pluses_2 = VGroup(
            *[
                MathTex("+").set_color(BLACK).scale(0.3).move_to(
                    sum_group_aux_2[k].get_right() + 0.5 * (sum_group_aux_2[k+1].get_left() - sum_group_aux_2[k].get_right())
                )
                for k in range(8)
            ]
        )

        self.play(
            sum_group_2.animate.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.1*UP + 3*RIGHT), #.align_to(hidden_layer[0][0], 2*UP+2*LEFT)
            # sum_group[5].animate.set_color(BLACK),
            FadeIn(pluses_2) 
        )

        brace_sum_2 = Brace(sum_group_2, UP, stroke_width=0.2, buff=0).set_color(BLACK).stretch_to_fit_height(0.1).shift(DOWN*0.05)
        brace_sum_text_2 = brace_sum_2.get_tex(r"100 \ \texttt{summands}").set_color(BLACK).scale(0.4).next_to(brace_sum_2, UP, buff=0.1)

        self.play(
            FadeIn(
                brace_sum_2, brace_sum_text_2
            )
        )

        self.wait()

        bias_num_2 = MathTex(
            "2.2", "+",
            color=RED_E
        ).scale(0.35).next_to(sum_group_aux_2, LEFT, buff=0.05)

        self.play(
            ReplacementTransform(
                output_layer[0][0].copy(),
                bias_num_2
            )
        )

        text_bias_2 = Tex(r"\texttt{Bias}").scale(0.4).set_color(RED_E).next_to(bias_num_2[0], UP, buff=0.15)

        self.play(
            FadeIn(text_bias_2)
        )

        self.wait()

        bra_left_2 = MathTex("[").set_color(DARK_BROWN).scale(0.4).next_to(bias_num_2, LEFT, buff=0.05)
        bra_right_2 = MathTex("]").set_color(DARK_BROWN).scale(0.4).next_to(sum_group_aux_2, RIGHT, buff=0.05)

        text_func_2 = MathTex(r"\sigma").scale(0.4).set_color(DARK_BROWN).next_to(bra_left_2, LEFT, buff=0.05)

        self.play(
            FadeIn(
                bra_left_2, bra_right_2, text_func_2
            )
        )
        self.wait()

        hidden_input_num_2 = MathTex(
            "=", "0.6",
        ).set_color(BLACK).scale(0.45).next_to(sum_group_2[4], DOWN, buff=0.25)

        self.play(
            FadeIn(hidden_input_num_2)
        )
        self.wait()

        self.play(
            hidden_input_num_2[1].copy().animate.scale(0.6).move_to(output_layer[0].get_center())
        )
        self.wait()

        self.play(
            LaggedStart(
                FadeOut(
                    sum_group_2, hidden_input_num_2, text_func_2, text_bias_2, pluses_2, bra_left_2, bra_right_2, bias_num_2, brace_sum_2, brace_sum_text_2
                ),
                self.camera.frame.animate.scale(2.25).move_to(hidden_layer.get_center()),
                lag_ratio=0.5
            )
        )
        self.wait()

        lines_aux_2 = lines_2.copy()
        lines_aux_2.set_color(GREEN_E).set_opacity(1)

        solo_lines_2 = VGroup()

        for group in lines_aux_2:
            for line in group:
                solo_lines_2.add(line)

        self.play(
            *[
                Create(line) for line in solo_lines_2
            ]
        )

        for line in solo_lines_2:
            line.reverse_points()

        first_lines_2.set_color(BLACK).set_opacity(0.1)

        output_layer_vals = [
            0.0, 0.1, 0.0, 0.0, 0.2, 0.0, 0.1, 0.0, 0.0
        ]

        output_layer_numbers = VGroup(
            *[
                DecimalNumber(
                    output_layer_vals[k],
                    color=BLACK,
                    num_decimal_places=1
                ).scale(0.3).move_to(output_layer[k+1].get_center())
                for k in range(9)
            ]
        )

        self.play(
            *[
                Uncreate(line) for line in solo_lines_2
            ],
            output_layer.animate.set_style(stroke_color=GREEN_E, stroke_opacity=1),
            VGroup(
                hidden_layer[0], hidden_layer[-1],
            ).animate.set_style(stroke_color=BLACK, stroke_opacity=0.2),
            FadeIn(
                output_layer_numbers
            )
            # rate_func = lambda t: smooth(t)
        )
        self.wait()


class ConveyerBeltNumbers_eng_v2(MovingCameraScene):
    def construct(self):

        self.camera.background_color = WHITE

        d_buffer = 1

        # text_input = Tex(r"\texttt{Input-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        # text_hl = Tex(r"\texttt{Hidden-Layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        # text_output = Tex(r"\texttt{Output-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        # text_hl_2 = Tex(r"(", r"100", r" \ \texttt{Neuronen})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        text_input = Tex(r"\texttt{Input layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        text_hl = Tex(r"\texttt{Hidden layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        text_output = Tex(r"\texttt{Output layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        text_hl_2 = Tex(r"(", r"100", r" \ \texttt{neurons})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        d1 = config["frame_height"]/2 - text_input.get_bottom()[1]

        input_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(9)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        input_layer_2 = input_layer_1.copy()

        dots = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.4)

        input_layer = VGroup(
            input_layer_1, dots, input_layer_2
        ).arrange(DOWN, buff=0.4).set_x(-config["frame_width"]/4 - d_buffer).set_y(-d1/2)

        hidden_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(7)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        dots_2 = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.2)
        
        hidden_layer = VGroup(
            hidden_layer_1, dots_2, hidden_layer_1.copy()
        ).arrange(DOWN, buff=0.2).set_y(-d1/2)

        output_layer = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(10)]
        ).arrange(DOWN, buff=0.2).scale(0.13).set_x(config["frame_width"]/4 + d_buffer).set_y(-d1/2)

        brace_input = Brace(input_layer, LEFT).set_color(BLACK)
        brace_input_text = brace_input.get_tex(r"784").set_color(BLACK)

        brace_output = Brace(output_layer, RIGHT).set_color(BLACK)
        brace_output_text = brace_output.get_tex(r"10").set_color(BLACK)

        lines = VGroup()
        hidden_layer_neurons = VGroup(*hidden_layer[0], *hidden_layer[-1])

        for j in [0,2]:
            for k in range(9):
                lines_k = VGroup(
                    *[Line(input_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in hidden_layer_neurons]
                )

                lines.add(lines_k)

        lines_2 = VGroup()

        for j in [0,2]:
            for k in range(7):
                lines_k = VGroup(
                    *[Line(hidden_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in output_layer]
                )

                lines_2.add(lines_k)

        self.add(
            input_layer, hidden_layer, output_layer, text_input, text_hl, text_hl_2, text_output, brace_input, brace_input_text, brace_output, brace_output_text, lines, lines_2
        )
        self.wait()

        self.play(
            self.camera.frame.animate.scale(0.4).move_to(input_layer[0].get_center()+2.3*RIGHT)
        )
        self.wait()

        self.play(
            VGroup(
                input_layer[1], hidden_layer[1], text_input, text_hl, text_hl_2, text_output, brace_input, brace_input_text, brace_output, brace_output_text, lines, lines_2
            ).animate.set_opacity(0.2),
            VGroup(
                input_layer[0], input_layer[-1], hidden_layer[0], hidden_layer[-1], output_layer,
            ).animate.set_style(stroke_opacity=0.2),
            input_layer[0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),
            input_layer[-1].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),

        )
        self.wait()

        input_values = [
            0.0, 0.0, 0.1, 0.2, 0.2, 0.7, 1.0, 0.7, 0.2
        ]

        weight_values = [
            2.0, -3.0, 2.5, 8.0, -2.5, -2.0, 5.0, 7.0, -0.5
        ]

        input_numbers = VGroup(
            *[
                DecimalNumber(
                    input_values[k],
                    num_decimal_places=1,
                    color=BLACK
                ).set_color(BLACK).scale(0.3).move_to(input_layer[0][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(9)
            ]
        )

        self.play(
            FadeIn(input_numbers)
        )
        self.wait()

        first_lines = VGroup(
            *[lines[k][0] for k in range(18)]
        )

        self.play(
            lines.animate.set_opacity(0.1),
        )
        self.play(
            hidden_layer[0][0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),
            first_lines.animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            )
        )
        self.wait()

        self.play(
            *[
                input_numbers[k].animate.move_to(first_lines[k].point_from_proportion(0.175))
                for k in range(9)
            ]
        )
        self.wait()

        x_aux_1 = VGroup(
            Dot(color=BLACK).scale(0.12),
            MathTex(
                "(-2.5)",
                color=RED_E,
            ).scale(0.3),
        ).arrange(RIGHT, buff=0.03).next_to(input_numbers[0], RIGHT, buff=0.03).get_x()

        m_dots = VGroup(
            *[
                
                Dot(
                    color=BLACK
                ).scale(0.12).next_to(input_numbers[k], RIGHT, buff=0.03).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        weight_equations = VGroup(
            *[
                VGroup(
                    # Dot(color=BLACK).scale(0.12),
                    # DecimalNumber(
                    #     weight_values[k],
                    #     num_decimal_places=1,
                    #     color=RED_E
                    # ).scale(0.3) 
                    MathTex(
                        "{}".format(weight_values[k]),
                        color=RED_E,
                    ).scale(0.3) if weight_values[k]>0 else
                    MathTex(
                        "({})".format(weight_values[k]),
                        color=RED_E,
                    ).scale(0.3),
                ).arrange(RIGHT, buff=0.03).next_to(m_dots[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        # x_aux_decimal_point = weight_equations[5][2].get_x()

        # x_aux_decimal_point = weight_equations[1][0][3].get_x()

        shift_vals = [
            0.17, 0, 0.17, 0.17, 0, 0, 0.17, 0.17, 0
        ]

        for k in range(9):
            weight_equations[k].shift(RIGHT*shift_vals[k])

        # for k in range(9):
        #     x_aux = weight_equations[k][1].get_x()
        #     shift_val = x_aux - x_aux_decimal_point
        #     weight_equations[k][2].shift( RIGHT )

        self.play(
            FadeIn(m_dots),
            FadeIn(weight_equations)
        )
        self.wait()

        text_weights = Tex(r"\texttt{Weights}").scale(0.4).set_color(RED_E).next_to(weight_equations, UP, buff=0.15)

        self.play(
            LaggedStart(
                FadeIn(text_weights),
                Circumscribe(weight_equations, color=RED_E, buff=0.02, time_width=2, run_time=3, stroke_width=2),
                lag_ratio=0.5
            )
        )
        self.wait()

        middle_numbers = VGroup(
            *[
                DecimalNumber(
                    input_values[k]*weight_values[k],
                    num_decimal_places=1,
                    color=BLACK
                ).set_color(BLACK).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        middle_numbers_2_vals = [
            -4.2, 3, 12.2, 0.7, -0.2, -2.2, 9.6, 0.0, 0.0
        ]

        middle_numbers_2 = VGroup(
            *[
                DecimalNumber(
                    middle_numbers_2_vals[k],
                    num_decimal_places=1,
                    color=BLACK
                ).set_color(BLACK).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE).move_to(first_lines[k+9].point_from_proportion(0.3))
                for k in range(9)
            ]
        )
        self.add(middle_numbers_2)

        equals_group = VGroup(
            *[
                MathTex("=").set_color(BLACK).scale(0.3).next_to(weight_equations[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        x_equal_aux = equals_group[-1].get_x()

        for sign in equals_group:
            sign.set_x(x_equal_aux)

        weight_solutions = VGroup(
            *[
                middle_numbers[k].next_to(equals_group[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        x_dp_aux = middle_numbers[4][3].get_x()

        dp_placement = [
            2, 2, 2, 2, 3, 3, 2, 2, 3
        ]

        for k in range(9):
            x_diff = middle_numbers[k][dp_placement[k]].get_x() - x_dp_aux
            weight_solutions[k].shift(LEFT*x_diff)

        self.play(
            FadeIn(equals_group),
            FadeIn(weight_solutions)
        )
        self.wait()

        self.play(
            FadeOut(
                text_weights, input_numbers, weight_equations, m_dots, equals_group, *[weight_solutions[k][:2] for k in range(9)]
            )
        )
        self.play(
            *[
                middle_numbers[k].animate.move_to(first_lines[k].point_from_proportion(0.99)).scale(0.5)
                for k in range(9)
            ],
            *[
                middle_numbers_2[k].animate.move_to(first_lines[k+9].point_from_proportion(0.99)).scale(0.5)
                for k in range(9)
            ],
            self.camera.frame.animate.set_x(2),
            run_time=2
        )

        dots_eq = VGroup(
            *[Dot(color=BLACK).scale(0.075) for _ in range(3)]
        ).arrange(RIGHT, buff=0.04).move_to(hidden_layer[0][0].get_left())

        for num in middle_numbers:
            if num.get_value()<0:
                val = num.get_value()
                num.become(
                    MathTex("( {} )".format(val)).set_color(BLACK).scale(0.3).scale(0.5),
                    match_center=True,
                )
        
        for num in middle_numbers_2:
            if num.get_value()<0:
                val = num.get_value()
                num.become(
                    MathTex("( {} )".format(val)).set_color(BLACK).scale(0.3).scale(0.5),
                    match_center=True,
                )

        self.remove(
            middle_numbers[5]
        )
        self.remove(
            middle_numbers[6]
        )
        self.remove(
            middle_numbers[7]
        )
        self.remove(
            middle_numbers[8]
        )
        self.remove(
            middle_numbers_2[0]
        )
        self.remove(
            middle_numbers_2[1]
        )
        self.remove(
            middle_numbers_2[2]
        )
        self.remove(
            middle_numbers_2[3]
        )

        sum_group = VGroup(
            *[middle_numbers[k] for k in range(5)],
            dots_eq,
            *[middle_numbers_2[k] for k in range(4,9)]
        )

        sum_group_aux = sum_group.copy()
        sum_group_aux.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.3*UP + 2*RIGHT)
        pluses = VGroup(
            *[
                MathTex("+").set_color(BLACK).scale(0.3).move_to(
                    sum_group_aux[k].get_right() + 0.5 * (sum_group_aux[k+1].get_left() - sum_group_aux[k].get_right())
                )
                for k in range(10)
            ]
        )


        self.play(
            sum_group.animate.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.3*UP + 2*RIGHT), #.align_to(hidden_layer[0][0], 2*UP+2*LEFT)
            # sum_group[5].animate.set_color(BLACK),
            FadeIn(pluses) 
        )

        brace_sum = Brace(sum_group, UP, stroke_width=0.2, buff=0.03).set_color(BLACK).stretch_to_fit_height(0.1)
        brace_sum_text = brace_sum.get_tex(r"784 \ \texttt{summands}").set_color(BLACK).scale(0.4).next_to(brace_sum, UP, buff=0.1)

        self.play(
            FadeIn(
                brace_sum, brace_sum_text
            )
        )

        self.wait()

        bias_num = MathTex(
            "+", "1.7",
            color=RED_E
        ).scale(0.3).next_to(sum_group_aux, RIGHT, buff=0.05)

        self.play(
            ReplacementTransform(
                hidden_layer[0][0].copy(),
                bias_num
            )
        )

        text_bias = Tex(r"\texttt{Bias}").scale(0.4).set_color(RED_E).next_to(bias_num[1], UP, buff=0.15)

        self.play(
            FadeIn(text_bias)
        )

        self.wait()

        bra_left = MathTex("(").set_color(DARK_BROWN).scale(0.5).next_to(sum_group_aux, LEFT, buff=0.05)
        bra_right = MathTex(")").set_color(DARK_BROWN).scale(0.5).next_to(bias_num, RIGHT, buff=0.05)

        text_func = Tex(r"\texttt{ReLU}").scale(0.4).set_color(DARK_BROWN).next_to(bra_left, LEFT, buff=0.05)

        self.play(
            FadeIn(
                bra_left, bra_right, text_func
            )
        )
        self.wait()

        hidden_input_num = MathTex(
            "=", "8.7",
        ).set_color(BLACK).scale(0.3).next_to(sum_group[4], DOWN, buff=0.15)

        self.play(
            FadeIn(hidden_input_num)
        )
        self.wait()

        hidden_layer_inputs_vals = [
            8.7, 5.3, 0.0, 0.0, 1.4, 1.2, 4.9, 2.2, 0.0, 9.4, 7.8, 0.0, 6.0, 0.0
        ]

        hidden_layer_inputs_1 = VGroup(
            *[
                DecimalNumber(
                    hidden_layer_inputs_vals[k],
                    color=BLACK,
                    num_decimal_places=1
                ).set_color(BLACK).scale(0.3).move_to(hidden_layer[0][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )
        hidden_layer_inputs_2 = VGroup(
            *[
                DecimalNumber(
                    hidden_layer_inputs_vals[k+7],
                    color=BLACK,
                    num_decimal_places=1
                ).set_color(BLACK).scale(0.3).move_to(hidden_layer[-1][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )

        self.play(
            #hidden_input_num[1].copy().animate.scale(0.8).move_to(hidden_layer[0][0].get_center())
            ReplacementTransform(
                hidden_input_num[1].copy(),
                hidden_layer_inputs_1[0]
            )
        )
        self.wait()


        self.play(
            LaggedStart(
                FadeOut(
                    sum_group, hidden_input_num, text_func, text_bias, pluses, bra_left, bra_right, bias_num, brace_sum, brace_sum_text
                ),
                self.camera.frame.animate.scale(2.25).move_to(hidden_layer.get_center()),
                lag_ratio=0.5
            )
        )
        self.wait()

        lines_aux = lines.copy()
        lines_aux.set_color(GREEN_E).set_opacity(1)

        solo_lines = VGroup()

        for group in lines_aux:
            for line in group:
                solo_lines.add(line)

        self.play(
            *[
                Create(line) for line in solo_lines
            ]
        )

        for line in solo_lines:
            line.reverse_points()

        first_lines.set_color(BLACK).set_opacity(0.1)

        self.play(
            *[
                Uncreate(line) for line in solo_lines
            ],
            VGroup(
                hidden_layer[0], hidden_layer[-1],
            ).animate.set_style(stroke_color=GREEN_E, stroke_opacity=1),
            VGroup(
                input_layer[0], input_layer[-1],
            ).animate.set_style(stroke_color=BLACK, stroke_opacity=0.2),
            FadeIn(
                hidden_layer_inputs_1[1:], hidden_layer_inputs_2
            )
            # rate_func = lambda t: smooth(t)
        )
        self.wait(2)

        first_lines_2 = VGroup(
            *[lines_2[k][0] for k in range(14)]
        )

        self.play(
            self.camera.frame.animate.scale(0.4).shift(RIGHT*2.25).set_y(hidden_layer[0].get_y()),
            lines_2.animate.set_opacity(0.1)
        )
        self.play(
            first_lines_2.animate.set_opacity(1).set_color(GREEN_E),
            output_layer[0].animate.set_stroke(color=GREEN_E, opacity=1),
        )
        self.wait()

        ################################################################################################################################

        weight_values_2 = [
            3.0, 7.0, -0.5, 9.0, -1.0, -2.0, -8.0
        ]


        self.play(
            *[
                hidden_layer_inputs_1[k].animate.move_to(first_lines_2[k].point_from_proportion(0.175))
                for k in range(7)
            ]
        )
        self.wait()

        m_dots_2 = VGroup(
            *[
                Dot(
                    color=BLACK
                ).scale(0.12).next_to(hidden_layer_inputs_1[k], RIGHT, buff=0.03).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        weight_equations_2 = VGroup(
            *[
                VGroup(
                    DecimalNumber(
                        weight_values_2[k],
                        num_decimal_places=1,
                        color=RED_E
                    ).scale(0.3) if weight_values_2[k]>0 else
                    MathTex(
                        "({})".format(weight_values_2[k]),
                        color=RED_E,
                    ).scale(0.3),
                ).arrange(RIGHT, buff=0.03).next_to(m_dots_2[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        shift_vals_3 = [
            0.165, 0.165, 0, 0.165, 0, 0, 0,
        ]

        for k in range(7):
            weight_equations_2[k].shift(RIGHT*shift_vals_3[k])

        self.play(
            FadeIn(m_dots_2),
            FadeIn(weight_equations_2)
        )
        self.wait()

        text_weights_2 = Tex(r"\texttt{Weights}").scale(0.4).set_color(RED_E).next_to(weight_equations_2, UP, buff=0.15)

        self.play(
            LaggedStart(
                FadeIn(text_weights_2),
                Circumscribe(weight_equations_2, color=RED_E, buff=0.02, time_width=2, run_time=3, stroke_width=2),
                lag_ratio=0.5
            )
        )
        self.wait()


        middle_numbers_2 = VGroup(
            *[
                DecimalNumber(
                    hidden_layer_inputs_vals[k]*weight_values_2[k],
                    num_decimal_places=1,
                    color=BLACK
                ).set_color(BLACK).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        middle_numbers_2_2_vals = [
            -6.9, 3, 0.0, 0.7, -0.2, 0.0, 3.1
        ]

        middle_numbers_2_2 = VGroup(
            *[
                DecimalNumber(
                    middle_numbers_2_2_vals[k],
                    num_decimal_places=1,
                    color=BLACK
                ).set_color(BLACK).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE).move_to(first_lines_2[k+7].point_from_proportion(0.175))
                for k in range(7)
            ]
        )
        self.add(middle_numbers_2_2)


        equals_group_2 = VGroup(
            *[
                MathTex("=").set_color(BLACK).scale(0.3).next_to(weight_equations_2[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        x_equal_aux_2 = equals_group_2[2].get_x()

        for sign in equals_group_2:
            sign.set_x(x_equal_aux_2)

        weight_solutions_2 = VGroup(
            *[
                middle_numbers_2[k].next_to(equals_group_2[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        x_dp_aux_2 = middle_numbers_2[-1][4].get_x()

        dp_placement = [
            3, 3, 2, 2, 3, 3, 4
        ]

        for k in range(7):
            x_diff = x_dp_aux_2 - middle_numbers_2[k][dp_placement[k]].get_x()
            weight_solutions_2[k].shift(RIGHT*x_diff)


        self.play(
            FadeIn(equals_group_2),
            FadeIn(weight_solutions_2)
        )
        self.wait()


        self.play(
            FadeOut(
                text_weights_2, hidden_layer_inputs_1, hidden_layer_inputs_2, weight_equations_2, m_dots_2, equals_group_2, *[weight_solutions_2[k][:2] for k in range(7)]
            )
        )
        self.play(
            *[
                middle_numbers_2[k].animate.move_to(first_lines_2[k].point_from_proportion(0.99)).scale(0.5)
                for k in range(7)
            ],
            *[
                middle_numbers_2_2[k].animate.move_to(first_lines_2[k+7].point_from_proportion(0.99)).scale(0.5)
                for k in range(7)
            ],
            run_time=1
        )
        #self.wait()

        dots_eq_2 = VGroup(
            *[Dot(color=BLACK).scale(0.075) for _ in range(3)]
        ).arrange(RIGHT, buff=0.04).move_to(output_layer[0].get_left())

        for num in middle_numbers_2:
            if num.get_value()<0:
                val = num.get_value()
                num.become(
                    MathTex("( {} )".format(val)).set_color(BLACK).scale(0.3).scale(0.5),
                    match_center=True,
                )
        
        for num in middle_numbers_2_2:
            if num.get_value()<0:
                val = num.get_value()
                num.become(
                    MathTex("( {} )".format(val)).set_color(BLACK).scale(0.3).scale(0.5),
                    match_center=True,
                )

        self.remove(
            middle_numbers_2[4]
        )
        self.remove(
            middle_numbers_2[5]
        )
        self.remove(
            middle_numbers_2[6]
        )
        self.remove(
            middle_numbers_2_2[0]
        )
        self.remove(
            middle_numbers_2_2[1]
        )
        self.remove(
            middle_numbers_2_2[2]
        )


        sum_group_2 = VGroup(
            *[middle_numbers_2[k] for k in range(4)],
            dots_eq_2,
            *[middle_numbers_2_2[k] for k in range(3,7)]
        )

        sum_group_aux_2 = sum_group_2.copy()
        sum_group_aux_2.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.1*UP + 2.5*RIGHT)
        pluses_2 = VGroup(
            *[
                MathTex("+").set_color(BLACK).scale(0.3).move_to(
                    sum_group_aux_2[k].get_right() + 0.5 * (sum_group_aux_2[k+1].get_left() - sum_group_aux_2[k].get_right())
                )
                for k in range(8)
            ]
        )

        self.play(
            sum_group_2.animate.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.1*UP + 2.5*RIGHT), #.align_to(hidden_layer[0][0], 2*UP+2*LEFT)
            # sum_group[5].animate.set_color(BLACK),
            FadeIn(pluses_2) 
        )

        brace_sum_2 = Brace(sum_group_2, UP, stroke_width=0.2, buff=0).set_color(BLACK).stretch_to_fit_height(0.1).shift(DOWN*0.05)
        brace_sum_text_2 = brace_sum_2.get_tex(r"100 \ \texttt{summands}").set_color(BLACK).scale(0.4).next_to(brace_sum_2, UP, buff=0.1)

        self.play(
            FadeIn(
                brace_sum_2, brace_sum_text_2
            )
        )

        self.wait()

        bias_num_2 = MathTex(
            "+", "2.2",
            color=RED_E
        ).scale(0.35).next_to(sum_group_aux_2, RIGHT, buff=0.05)

        self.play(
            ReplacementTransform(
                output_layer[0][0].copy(),
                bias_num_2
            )
        )

        text_bias_2 = Tex(r"\texttt{Bias}").scale(0.4).set_color(RED_E).next_to(bias_num_2[1], UP, buff=0.15)

        self.play(
            FadeIn(text_bias_2)
        )

        self.wait()

        bra_left_2 = MathTex("[").set_color(DARK_BROWN).scale(0.4).next_to(bias_num_2, LEFT, buff=0.05)
        bra_right_2 = MathTex("]").set_color(DARK_BROWN).scale(0.4).next_to(sum_group_aux_2, RIGHT, buff=0.05)

        text_func_2 = MathTex(r"\sigma").scale(0.4).set_color(DARK_BROWN).next_to(bra_left_2, LEFT, buff=0.05)

        # self.play(
        #     FadeIn(
        #         bra_left_2, bra_right_2, text_func_2
        #     )
        # )
        # self.wait()

        hidden_input_num_2 = MathTex(
            "=", "0.6",
        ).set_color(BLACK).scale(0.45).next_to(sum_group_2[4], DOWN, buff=0.25)

        self.play(
            FadeIn(hidden_input_num_2)
        )
        self.wait()

        hidden_input_num_2_aux = hidden_input_num_2[1].copy()


        self.play(
            hidden_input_num_2_aux.animate.scale(0.6).move_to(output_layer[0].get_center())
        )
        self.wait()

        self.play(
            LaggedStart(
                FadeOut(
                    sum_group_2, hidden_input_num_2, text_bias_2, pluses_2, bias_num_2, brace_sum_2, brace_sum_text_2
                ),
                self.camera.frame.animate.scale(2.25).move_to(hidden_layer.get_center()),
                lag_ratio=0.5
            )
        )
        self.wait()

        lines_aux_2 = lines_2.copy()
        lines_aux_2.set_color(GREEN_E).set_opacity(1)

        solo_lines_2 = VGroup()

        for group in lines_aux_2:
            for line in group:
                solo_lines_2.add(line)

        self.play(
            *[
                Create(line) for line in solo_lines_2
            ]
        )

        for line in solo_lines_2:
            line.reverse_points()

        first_lines_2.set_color(BLACK).set_opacity(0.1)

        output_layer_vals = [
            4.0, -7.5, 3.3, -0.2, 5.3, 4.1, 3.0, -5.2, 0.2
        ]

        output_layer_numbers = VGroup(
            *[
                DecimalNumber(
                    output_layer_vals[k],
                    color=BLACK,
                    num_decimal_places=1
                ).set_color(BLACK).scale(0.3).move_to(output_layer[k+1].get_center())
                for k in range(9)
            ]
        )

        self.play(
            *[
                Uncreate(line) for line in solo_lines_2
            ],
            output_layer.animate.set_style(stroke_color=GREEN_E, stroke_opacity=1),
            VGroup(
                hidden_layer[0], hidden_layer[-1],
            ).animate.set_style(stroke_color=BLACK, stroke_opacity=0.2),
            FadeIn(
                output_layer_numbers
            )
            # rate_func = lambda t: smooth(t)
        )
        self.wait()

        ###########

        output_layer_numbers_com = VGroup(
            hidden_input_num_2_aux, *output_layer_numbers
        )

        self.play(
            output_layer_numbers_com.animate.scale(2).arrange(RIGHT, buff=0.2).to_edge(UR, buff=2).shift(UP*0.75)
        )

        commas = VGroup(
            *[
                MathTex(",").scale(0.7).next_to(output_layer_numbers_com[i], buff=0.05).shift(DOWN*output_layer_numbers_com.get_height()*0.4)
                for i in range(9)
            ]
        ).set_color(BLACK)

        bra_left_2 = MathTex("[").set_color(BLACK).scale(0.75).next_to(output_layer_numbers_com, LEFT, buff=0.05)
        bra_right_2 = MathTex("]").set_color(BLACK).scale(0.75).next_to(output_layer_numbers_com, RIGHT, buff=0.03)


        self.play(
            FadeIn(commas, bra_left_2, bra_right_2)
        )
        self.wait(0.5)

        bra_left_2_2 = MathTex("(").set_color(DARK_BROWN).scale(1).next_to(bra_left_2, LEFT, buff=0.05)
        bra_right_2_2 = MathTex(")").set_color(DARK_BROWN).scale(1).next_to(bra_right_2, RIGHT, buff=0.05)
        text_func_2 = MathTex(r"\sigma").scale(0.8).set_color(DARK_BROWN).next_to(bra_left_2_2, LEFT, buff=0.05)

        self.play(
            FadeIn(bra_left_2_2, bra_right_2_2, text_func_2)
        )
        self.wait()

        final_vals = [0.0, 0.2, 0.0, 0.0, 0.0, 0.6, 0.2, 0.0 , 0.0, 0.0]

        output_layer_numbers_2 = VGroup(
            *[
                DecimalNumber(
                    final_vals[k],
                    num_decimal_places=1,
                    color=BLACK,
                ).set_color(BLACK).scale(0.6)
                for k in range(10)
            ]
        ).arrange(RIGHT, buff=0.2).next_to(output_layer_numbers_com, DOWN).to_edge(RIGHT, buff=1.75)
        commas_2 = VGroup(
            *[
                MathTex(",").scale(0.7).next_to(output_layer_numbers_2[i], buff=0.05).shift(DOWN*output_layer_numbers_2.get_height()*0.4)
                for i in range(9)
            ]
        ).set_color(BLACK)
        bra_left_2_3 = MathTex("=[").set_color(BLACK).scale(0.75).next_to(output_layer_numbers_2, LEFT, buff=0.05)
        bra_right_2_3 = MathTex("]").set_color(BLACK).scale(0.75).next_to(output_layer_numbers_2, RIGHT, buff=0.03)


        self.play(
            FadeIn(output_layer_numbers_2, commas_2, bra_left_2_3, bra_right_2_3)
        )
        self.wait()

        self.play(
            *[
                output_layer_numbers_2[i].copy().animate.scale(0.55).move_to(output_layer[i].get_center())
                for i in range(10)
            ]
        )
        self.wait()

        self.play(
            FadeOut(output_layer_numbers_2, output_layer_numbers_com, commas_2, bra_left_2_3, bra_right_2_3, bra_left_2_2, bra_right_2_2, text_func_2, commas, bra_left_2, bra_right_2)
        )
        self.wait()


class ConveyerBeltNumbers_ger_v2(MovingCameraScene):
    def construct(self):

        self.camera.background_color = WHITE

        d_buffer = 1

        # text_input = Tex(r"\texttt{Input-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        # text_hl = Tex(r"\texttt{Hidden-Layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        # text_output = Tex(r"\texttt{Output-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        # text_hl_2 = Tex(r"(", r"100", r" \ \texttt{Neuronen})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        text_input = Tex(r"\texttt{Input-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        text_hl = Tex(r"\texttt{Hidden-Layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        text_output = Tex(r"\texttt{Output-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        text_hl_2 = Tex(r"(", r"100", r" \ \texttt{Neuronen})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        d1 = config["frame_height"]/2 - text_input.get_bottom()[1]

        input_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(9)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        input_layer_2 = input_layer_1.copy()

        dots = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.4)

        input_layer = VGroup(
            input_layer_1, dots, input_layer_2
        ).arrange(DOWN, buff=0.4).set_x(-config["frame_width"]/4 - d_buffer).set_y(-d1/2)

        hidden_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(7)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        dots_2 = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.2)
        
        hidden_layer = VGroup(
            hidden_layer_1, dots_2, hidden_layer_1.copy()
        ).arrange(DOWN, buff=0.2).set_y(-d1/2)

        output_layer = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(10)]
        ).arrange(DOWN, buff=0.2).scale(0.13).set_x(config["frame_width"]/4 + d_buffer).set_y(-d1/2)

        brace_input = Brace(input_layer, LEFT).set_color(BLACK)
        brace_input_text = brace_input.get_tex(r"784").set_color(BLACK)

        brace_output = Brace(output_layer, RIGHT).set_color(BLACK)
        brace_output_text = brace_output.get_tex(r"10").set_color(BLACK)

        lines = VGroup()
        hidden_layer_neurons = VGroup(*hidden_layer[0], *hidden_layer[-1])

        for j in [0,2]:
            for k in range(9):
                lines_k = VGroup(
                    *[Line(input_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in hidden_layer_neurons]
                )

                lines.add(lines_k)

        lines_2 = VGroup()

        for j in [0,2]:
            for k in range(7):
                lines_k = VGroup(
                    *[Line(hidden_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in output_layer]
                )

                lines_2.add(lines_k)

        self.add(
            input_layer, hidden_layer, output_layer, text_input, text_hl, text_hl_2, text_output, brace_input, brace_input_text, brace_output, brace_output_text, lines, lines_2
        )
        self.wait()

        self.play(
            self.camera.frame.animate.scale(0.4).move_to(input_layer[0].get_center()+2.3*RIGHT)
        )
        self.wait()

        self.play(
            VGroup(
                input_layer[1], hidden_layer[1], text_input, text_hl, text_hl_2, text_output, brace_input, brace_input_text, brace_output, brace_output_text, lines, lines_2
            ).animate.set_opacity(0.2),
            VGroup(
                input_layer[0], input_layer[-1], hidden_layer[0], hidden_layer[-1], output_layer,
            ).animate.set_style(stroke_opacity=0.2),
            input_layer[0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),
            input_layer[-1].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),

        )
        self.wait()

        input_values = [
            0.0, 0.0, 0.1, 0.2, 0.2, 0.7, 1.0, 0.7, 0.2
        ]

        weight_values = [
            2.0, -3.0, 2.5, 8.0, -2.5, -2.0, 5.0, 7.0, -0.5
        ]

        input_numbers = VGroup(
            *[
                DecimalNumber(
                    input_values[k],
                    num_decimal_places=1,
                    color=BLACK
                ).set_color(BLACK).scale(0.3).move_to(input_layer[0][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(9)
            ]
        )

        self.play(
            FadeIn(input_numbers)
        )
        self.wait()

        first_lines = VGroup(
            *[lines[k][0] for k in range(18)]
        )

        self.play(
            lines.animate.set_opacity(0.1),
        )
        self.play(
            hidden_layer[0][0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),
            first_lines.animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            )
        )
        self.wait()

        self.play(
            *[
                input_numbers[k].animate.move_to(first_lines[k].point_from_proportion(0.175))
                for k in range(9)
            ]
        )
        self.wait()

        x_aux_1 = VGroup(
            Dot(color=BLACK).scale(0.12),
            MathTex(
                "(-2.5)",
                color=RED_E,
            ).scale(0.3),
        ).arrange(RIGHT, buff=0.03).next_to(input_numbers[0], RIGHT, buff=0.03).get_x()

        m_dots = VGroup(
            *[
                
                Dot(
                    color=BLACK
                ).scale(0.12).next_to(input_numbers[k], RIGHT, buff=0.03).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        weight_equations = VGroup(
            *[
                VGroup(
                    # Dot(color=BLACK).scale(0.12),
                    # DecimalNumber(
                    #     weight_values[k],
                    #     num_decimal_places=1,
                    #     color=RED_E
                    # ).scale(0.3) 
                    MathTex(
                        "{}".format(weight_values[k]),
                        color=RED_E,
                    ).scale(0.3) if weight_values[k]>0 else
                    MathTex(
                        "({})".format(weight_values[k]),
                        color=RED_E,
                    ).scale(0.3),
                ).arrange(RIGHT, buff=0.03).next_to(m_dots[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        # x_aux_decimal_point = weight_equations[5][2].get_x()

        # x_aux_decimal_point = weight_equations[1][0][3].get_x()

        shift_vals = [
            0.17, 0, 0.17, 0.17, 0, 0, 0.17, 0.17, 0
        ]

        for k in range(9):
            weight_equations[k].shift(RIGHT*shift_vals[k])

        # for k in range(9):
        #     x_aux = weight_equations[k][1].get_x()
        #     shift_val = x_aux - x_aux_decimal_point
        #     weight_equations[k][2].shift( RIGHT )

        self.play(
            FadeIn(m_dots),
            FadeIn(weight_equations)
        )
        self.wait()

        text_weights = Tex(r"\texttt{Gewichte}").scale(0.4).set_color(RED_E).next_to(weight_equations, UP, buff=0.15)

        self.play(
            LaggedStart(
                FadeIn(text_weights),
                Circumscribe(weight_equations, color=RED_E, buff=0.02, time_width=2, run_time=3, stroke_width=2),
                lag_ratio=0.5
            )
        )
        self.wait()

        middle_numbers = VGroup(
            *[
                DecimalNumber(
                    input_values[k]*weight_values[k],
                    num_decimal_places=1,
                    color=BLACK
                ).set_color(BLACK).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        middle_numbers_2_vals = [
            -4.2, 3, 12.2, 0.7, -0.2, -2.2, 9.6, 0.0, 0.0
        ]

        middle_numbers_2 = VGroup(
            *[
                DecimalNumber(
                    middle_numbers_2_vals[k],
                    num_decimal_places=1,
                    color=BLACK
                ).set_color(BLACK).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE).move_to(first_lines[k+9].point_from_proportion(0.3))
                for k in range(9)
            ]
        )
        self.add(middle_numbers_2)

        equals_group = VGroup(
            *[
                MathTex("=").set_color(BLACK).scale(0.3).next_to(weight_equations[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        x_equal_aux = equals_group[-1].get_x()

        for sign in equals_group:
            sign.set_x(x_equal_aux)

        weight_solutions = VGroup(
            *[
                middle_numbers[k].next_to(equals_group[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        x_dp_aux = middle_numbers[4][3].get_x()

        dp_placement = [
            2, 2, 2, 2, 3, 3, 2, 2, 3
        ]

        for k in range(9):
            x_diff = middle_numbers[k][dp_placement[k]].get_x() - x_dp_aux
            weight_solutions[k].shift(LEFT*x_diff)

        self.play(
            FadeIn(equals_group),
            FadeIn(weight_solutions)
        )
        self.wait()

        self.play(
            FadeOut(
                text_weights, input_numbers, weight_equations, m_dots, equals_group, *[weight_solutions[k][:2] for k in range(9)]
            )
        )
        self.play(
            *[
                middle_numbers[k].animate.move_to(first_lines[k].point_from_proportion(0.99)).scale(0.5)
                for k in range(9)
            ],
            *[
                middle_numbers_2[k].animate.move_to(first_lines[k+9].point_from_proportion(0.99)).scale(0.5)
                for k in range(9)
            ],
            self.camera.frame.animate.set_x(2),
            run_time=2
        )

        dots_eq = VGroup(
            *[Dot(color=BLACK).scale(0.075) for _ in range(3)]
        ).arrange(RIGHT, buff=0.04).move_to(hidden_layer[0][0].get_left())

        for num in middle_numbers:
            if num.get_value()<0:
                val = num.get_value()
                num.become(
                    MathTex("( {} )".format(val)).set_color(BLACK).scale(0.3).scale(0.5),
                    match_center=True,
                )
        
        for num in middle_numbers_2:
            if num.get_value()<0:
                val = num.get_value()
                num.become(
                    MathTex("( {} )".format(val)).set_color(BLACK).scale(0.3).scale(0.5),
                    match_center=True,
                )

        self.remove(
            middle_numbers[5]
        )
        self.remove(
            middle_numbers[6]
        )
        self.remove(
            middle_numbers[7]
        )
        self.remove(
            middle_numbers[8]
        )
        self.remove(
            middle_numbers_2[0]
        )
        self.remove(
            middle_numbers_2[1]
        )
        self.remove(
            middle_numbers_2[2]
        )
        self.remove(
            middle_numbers_2[3]
        )

        sum_group = VGroup(
            *[middle_numbers[k] for k in range(5)],
            dots_eq,
            *[middle_numbers_2[k] for k in range(4,9)]
        )

        sum_group_aux = sum_group.copy()
        sum_group_aux.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.3*UP + 2*RIGHT)
        pluses = VGroup(
            *[
                MathTex("+").set_color(BLACK).scale(0.3).move_to(
                    sum_group_aux[k].get_right() + 0.5 * (sum_group_aux[k+1].get_left() - sum_group_aux[k].get_right())
                )
                for k in range(10)
            ]
        )


        self.play(
            sum_group.animate.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.3*UP + 2*RIGHT), #.align_to(hidden_layer[0][0], 2*UP+2*LEFT)
            # sum_group[5].animate.set_color(BLACK),
            FadeIn(pluses) 
        )

        brace_sum = Brace(sum_group, UP, stroke_width=0.2, buff=0.03).set_color(BLACK).stretch_to_fit_height(0.1)
        brace_sum_text = brace_sum.get_tex(r"784 \ \texttt{Summanden}").set_color(BLACK).scale(0.4).next_to(brace_sum, UP, buff=0.1)

        self.play(
            FadeIn(
                brace_sum, brace_sum_text
            )
        )

        self.wait()

        bias_num = MathTex(
            "+", "1.7",
            color=RED_E
        ).scale(0.3).next_to(sum_group_aux, RIGHT, buff=0.05)

        self.play(
            ReplacementTransform(
                hidden_layer[0][0].copy(),
                bias_num
            )
        )

        text_bias = Tex(r"\texttt{Bias}").scale(0.4).set_color(RED_E).next_to(bias_num[1], UP, buff=0.15)

        self.play(
            FadeIn(text_bias)
        )

        self.wait()

        bra_left = MathTex("(").set_color(DARK_BROWN).scale(0.5).next_to(sum_group_aux, LEFT, buff=0.05)
        bra_right = MathTex(")").set_color(DARK_BROWN).scale(0.5).next_to(bias_num, RIGHT, buff=0.05)

        text_func = Tex(r"\texttt{ReLU}").scale(0.4).set_color(DARK_BROWN).next_to(bra_left, LEFT, buff=0.05)

        self.play(
            FadeIn(
                bra_left, bra_right, text_func
            )
        )
        self.wait()

        hidden_input_num = MathTex(
            "=", "8.7",
        ).set_color(BLACK).scale(0.3).next_to(sum_group[4], DOWN, buff=0.15)

        self.play(
            FadeIn(hidden_input_num)
        )
        self.wait()

        hidden_layer_inputs_vals = [
            8.7, 5.3, 0.0, 0.0, 1.4, 1.2, 4.9, 2.2, 0.0, 9.4, 7.8, 0.0, 6.0, 0.0
        ]

        hidden_layer_inputs_1 = VGroup(
            *[
                DecimalNumber(
                    hidden_layer_inputs_vals[k],
                    color=BLACK,
                    num_decimal_places=1
                ).set_color(BLACK).scale(0.3).move_to(hidden_layer[0][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )
        hidden_layer_inputs_2 = VGroup(
            *[
                DecimalNumber(
                    hidden_layer_inputs_vals[k+7],
                    color=BLACK,
                    num_decimal_places=1
                ).set_color(BLACK).scale(0.3).move_to(hidden_layer[-1][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )

        self.play(
            #hidden_input_num[1].copy().animate.scale(0.8).move_to(hidden_layer[0][0].get_center())
            ReplacementTransform(
                hidden_input_num[1].copy(),
                hidden_layer_inputs_1[0]
            )
        )
        self.wait()


        self.play(
            LaggedStart(
                FadeOut(
                    sum_group, hidden_input_num, text_func, text_bias, pluses, bra_left, bra_right, bias_num, brace_sum, brace_sum_text
                ),
                self.camera.frame.animate.scale(2.25).move_to(hidden_layer.get_center()),
                lag_ratio=0.5
            )
        )
        self.wait()

        lines_aux = lines.copy()
        lines_aux.set_color(GREEN_E).set_opacity(1)

        solo_lines = VGroup()

        for group in lines_aux:
            for line in group:
                solo_lines.add(line)

        self.play(
            *[
                Create(line) for line in solo_lines
            ]
        )

        for line in solo_lines:
            line.reverse_points()

        first_lines.set_color(BLACK).set_opacity(0.1)

        self.play(
            *[
                Uncreate(line) for line in solo_lines
            ],
            VGroup(
                hidden_layer[0], hidden_layer[-1],
            ).animate.set_style(stroke_color=GREEN_E, stroke_opacity=1),
            VGroup(
                input_layer[0], input_layer[-1],
            ).animate.set_style(stroke_color=BLACK, stroke_opacity=0.2),
            FadeIn(
                hidden_layer_inputs_1[1:], hidden_layer_inputs_2
            )
            # rate_func = lambda t: smooth(t)
        )
        self.wait(2)

        first_lines_2 = VGroup(
            *[lines_2[k][0] for k in range(14)]
        )

        self.play(
            self.camera.frame.animate.scale(0.4).shift(RIGHT*2.25).set_y(hidden_layer[0].get_y()),
            lines_2.animate.set_opacity(0.1)
        )
        self.play(
            first_lines_2.animate.set_opacity(1).set_color(GREEN_E),
            output_layer[0].animate.set_stroke(color=GREEN_E, opacity=1),
        )
        self.wait()

        ################################################################################################################################

        weight_values_2 = [
            3.0, 7.0, -0.5, 9.0, -1.0, -2.0, -8.0
        ]


        self.play(
            *[
                hidden_layer_inputs_1[k].animate.move_to(first_lines_2[k].point_from_proportion(0.175))
                for k in range(7)
            ]
        )
        self.wait()

        m_dots_2 = VGroup(
            *[
                Dot(
                    color=BLACK
                ).scale(0.12).next_to(hidden_layer_inputs_1[k], RIGHT, buff=0.03).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        weight_equations_2 = VGroup(
            *[
                VGroup(
                    DecimalNumber(
                        weight_values_2[k],
                        num_decimal_places=1,
                        color=RED_E
                    ).scale(0.3) if weight_values_2[k]>0 else
                    MathTex(
                        "({})".format(weight_values_2[k]),
                        color=RED_E,
                    ).scale(0.3),
                ).arrange(RIGHT, buff=0.03).next_to(m_dots_2[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        shift_vals_3 = [
            0.165, 0.165, 0, 0.165, 0, 0, 0,
        ]

        for k in range(7):
            weight_equations_2[k].shift(RIGHT*shift_vals_3[k])

        self.play(
            FadeIn(m_dots_2),
            FadeIn(weight_equations_2)
        )
        self.wait()

        text_weights_2 = Tex(r"\texttt{Gewichte}").scale(0.4).set_color(RED_E).next_to(weight_equations_2, UP, buff=0.15)

        self.play(
            LaggedStart(
                FadeIn(text_weights_2),
                Circumscribe(weight_equations_2, color=RED_E, buff=0.02, time_width=2, run_time=3, stroke_width=2),
                lag_ratio=0.5
            )
        )
        self.wait()


        middle_numbers_2 = VGroup(
            *[
                DecimalNumber(
                    hidden_layer_inputs_vals[k]*weight_values_2[k],
                    num_decimal_places=1,
                    color=BLACK
                ).set_color(BLACK).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        middle_numbers_2_2_vals = [
            -6.9, 3, 0.0, 0.7, -0.2, 0.0, 3.1
        ]

        middle_numbers_2_2 = VGroup(
            *[
                DecimalNumber(
                    middle_numbers_2_2_vals[k],
                    num_decimal_places=1,
                    color=BLACK
                ).set_color(BLACK).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE).move_to(first_lines_2[k+7].point_from_proportion(0.175))
                for k in range(7)
            ]
        )
        self.add(middle_numbers_2_2)


        equals_group_2 = VGroup(
            *[
                MathTex("=").set_color(BLACK).scale(0.3).next_to(weight_equations_2[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        x_equal_aux_2 = equals_group_2[2].get_x()

        for sign in equals_group_2:
            sign.set_x(x_equal_aux_2)

        weight_solutions_2 = VGroup(
            *[
                middle_numbers_2[k].next_to(equals_group_2[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        x_dp_aux_2 = middle_numbers_2[-1][4].get_x()

        dp_placement = [
            3, 3, 2, 2, 3, 3, 4
        ]

        for k in range(7):
            x_diff = x_dp_aux_2 - middle_numbers_2[k][dp_placement[k]].get_x()
            weight_solutions_2[k].shift(RIGHT*x_diff)


        self.play(
            FadeIn(equals_group_2),
            FadeIn(weight_solutions_2)
        )
        self.wait()


        self.play(
            FadeOut(
                text_weights_2, hidden_layer_inputs_1, hidden_layer_inputs_2, weight_equations_2, m_dots_2, equals_group_2, *[weight_solutions_2[k][:2] for k in range(7)]
            )
        )
        self.play(
            *[
                middle_numbers_2[k].animate.move_to(first_lines_2[k].point_from_proportion(0.99)).scale(0.5)
                for k in range(7)
            ],
            *[
                middle_numbers_2_2[k].animate.move_to(first_lines_2[k+7].point_from_proportion(0.99)).scale(0.5)
                for k in range(7)
            ],
            run_time=1
        )
        #self.wait()

        dots_eq_2 = VGroup(
            *[Dot(color=BLACK).scale(0.075) for _ in range(3)]
        ).arrange(RIGHT, buff=0.04).move_to(output_layer[0].get_left())

        for num in middle_numbers_2:
            if num.get_value()<0:
                val = num.get_value()
                num.become(
                    MathTex("( {} )".format(val)).set_color(BLACK).scale(0.3).scale(0.5),
                    match_center=True,
                )
        
        for num in middle_numbers_2_2:
            if num.get_value()<0:
                val = num.get_value()
                num.become(
                    MathTex("( {} )".format(val)).set_color(BLACK).scale(0.3).scale(0.5),
                    match_center=True,
                )

        self.remove(
            middle_numbers_2[4]
        )
        self.remove(
            middle_numbers_2[5]
        )
        self.remove(
            middle_numbers_2[6]
        )
        self.remove(
            middle_numbers_2_2[0]
        )
        self.remove(
            middle_numbers_2_2[1]
        )
        self.remove(
            middle_numbers_2_2[2]
        )


        sum_group_2 = VGroup(
            *[middle_numbers_2[k] for k in range(4)],
            dots_eq_2,
            *[middle_numbers_2_2[k] for k in range(3,7)]
        )

        sum_group_aux_2 = sum_group_2.copy()
        sum_group_aux_2.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.1*UP + 2.5*RIGHT)
        pluses_2 = VGroup(
            *[
                MathTex("+").set_color(BLACK).scale(0.3).move_to(
                    sum_group_aux_2[k].get_right() + 0.5 * (sum_group_aux_2[k+1].get_left() - sum_group_aux_2[k].get_right())
                )
                for k in range(8)
            ]
        )

        self.play(
            sum_group_2.animate.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.1*UP + 2.5*RIGHT), #.align_to(hidden_layer[0][0], 2*UP+2*LEFT)
            # sum_group[5].animate.set_color(BLACK),
            FadeIn(pluses_2) 
        )

        brace_sum_2 = Brace(sum_group_2, UP, stroke_width=0.2, buff=0).set_color(BLACK).stretch_to_fit_height(0.1).shift(DOWN*0.05)
        brace_sum_text_2 = brace_sum_2.get_tex(r"100 \ \texttt{Summanden}").set_color(BLACK).scale(0.4).next_to(brace_sum_2, UP, buff=0.1)

        self.play(
            FadeIn(
                brace_sum_2, brace_sum_text_2
            )
        )

        self.wait()

        bias_num_2 = MathTex(
            "+", "2.2",
            color=RED_E
        ).scale(0.35).next_to(sum_group_aux_2, RIGHT, buff=0.05)

        self.play(
            ReplacementTransform(
                output_layer[0][0].copy(),
                bias_num_2
            )
        )

        text_bias_2 = Tex(r"\texttt{Bias}").scale(0.4).set_color(RED_E).next_to(bias_num_2[1], UP, buff=0.15)

        self.play(
            FadeIn(text_bias_2)
        )

        self.wait()

        bra_left_2 = MathTex("[").set_color(DARK_BROWN).scale(0.4).next_to(bias_num_2, LEFT, buff=0.05)
        bra_right_2 = MathTex("]").set_color(DARK_BROWN).scale(0.4).next_to(sum_group_aux_2, RIGHT, buff=0.05)

        text_func_2 = MathTex(r"\sigma").scale(0.4).set_color(DARK_BROWN).next_to(bra_left_2, LEFT, buff=0.05)

        # self.play(
        #     FadeIn(
        #         bra_left_2, bra_right_2, text_func_2
        #     )
        # )
        # self.wait()

        hidden_input_num_2 = MathTex(
            "=", "0.6",
        ).set_color(BLACK).scale(0.45).next_to(sum_group_2[4], DOWN, buff=0.25)

        self.play(
            FadeIn(hidden_input_num_2)
        )
        self.wait()

        hidden_input_num_2_aux = hidden_input_num_2[1].copy()


        self.play(
            hidden_input_num_2_aux.animate.scale(0.6).move_to(output_layer[0].get_center())
        )
        self.wait()

        self.play(
            LaggedStart(
                FadeOut(
                    sum_group_2, hidden_input_num_2, text_bias_2, pluses_2, bias_num_2, brace_sum_2, brace_sum_text_2
                ),
                self.camera.frame.animate.scale(2.25).move_to(hidden_layer.get_center()),
                lag_ratio=0.5
            )
        )
        self.wait()

        lines_aux_2 = lines_2.copy()
        lines_aux_2.set_color(GREEN_E).set_opacity(1)

        solo_lines_2 = VGroup()

        for group in lines_aux_2:
            for line in group:
                solo_lines_2.add(line)

        self.play(
            *[
                Create(line) for line in solo_lines_2
            ]
        )

        for line in solo_lines_2:
            line.reverse_points()

        first_lines_2.set_color(BLACK).set_opacity(0.1)

        output_layer_vals = [
            4.0, -7.5, 3.3, -0.2, 5.3, 4.1, 3.0, -5.2, 0.2
        ]

        output_layer_numbers = VGroup(
            *[
                DecimalNumber(
                    output_layer_vals[k],
                    color=BLACK,
                    num_decimal_places=1
                ).set_color(BLACK).scale(0.3).move_to(output_layer[k+1].get_center())
                for k in range(9)
            ]
        )

        self.play(
            *[
                Uncreate(line) for line in solo_lines_2
            ],
            output_layer.animate.set_style(stroke_color=GREEN_E, stroke_opacity=1),
            VGroup(
                hidden_layer[0], hidden_layer[-1],
            ).animate.set_style(stroke_color=BLACK, stroke_opacity=0.2),
            FadeIn(
                output_layer_numbers
            )
            # rate_func = lambda t: smooth(t)
        )
        self.wait()

        ###########

        output_layer_numbers_com = VGroup(
            hidden_input_num_2_aux, *output_layer_numbers
        )

        self.play(
            output_layer_numbers_com.animate.scale(2).arrange(RIGHT, buff=0.2).to_edge(UR, buff=2).shift(UP*0.75)
        )

        commas = VGroup(
            *[
                MathTex(",").scale(0.7).next_to(output_layer_numbers_com[i], buff=0.05).shift(DOWN*output_layer_numbers_com.get_height()*0.4)
                for i in range(9)
            ]
        ).set_color(BLACK)

        bra_left_2 = MathTex("[").set_color(BLACK).scale(0.75).next_to(output_layer_numbers_com, LEFT, buff=0.05)
        bra_right_2 = MathTex("]").set_color(BLACK).scale(0.75).next_to(output_layer_numbers_com, RIGHT, buff=0.03)


        self.play(
            FadeIn(commas, bra_left_2, bra_right_2)
        )
        self.wait(0.5)

        bra_left_2_2 = MathTex("(").set_color(DARK_BROWN).scale(1).next_to(bra_left_2, LEFT, buff=0.05)
        bra_right_2_2 = MathTex(")").set_color(DARK_BROWN).scale(1).next_to(bra_right_2, RIGHT, buff=0.05)
        text_func_2 = MathTex(r"\sigma").scale(0.8).set_color(DARK_BROWN).next_to(bra_left_2_2, LEFT, buff=0.05)

        self.play(
            FadeIn(bra_left_2_2, bra_right_2_2, text_func_2)
        )
        self.wait()

        final_vals = [0.0, 0.2, 0.0, 0.0, 0.0, 0.6, 0.2, 0.0 , 0.0, 0.0]

        output_layer_numbers_2 = VGroup(
            *[
                DecimalNumber(
                    final_vals[k],
                    num_decimal_places=1,
                    color=BLACK,
                ).set_color(BLACK).scale(0.6)
                for k in range(10)
            ]
        ).arrange(RIGHT, buff=0.2).next_to(output_layer_numbers_com, DOWN).to_edge(RIGHT, buff=1.75)
        commas_2 = VGroup(
            *[
                MathTex(",").scale(0.7).next_to(output_layer_numbers_2[i], buff=0.05).shift(DOWN*output_layer_numbers_2.get_height()*0.4)
                for i in range(9)
            ]
        ).set_color(BLACK)
        bra_left_2_3 = MathTex("=[").set_color(BLACK).scale(0.75).next_to(output_layer_numbers_2, LEFT, buff=0.05)
        bra_right_2_3 = MathTex("]").set_color(BLACK).scale(0.75).next_to(output_layer_numbers_2, RIGHT, buff=0.03)


        self.play(
            FadeIn(output_layer_numbers_2, commas_2, bra_left_2_3, bra_right_2_3)
        )
        self.wait()

        self.play(
            *[
                output_layer_numbers_2[i].copy().animate.scale(0.55).move_to(output_layer[i].get_center())
                for i in range(10)
            ]
        )
        self.wait()

        self.play(
            FadeOut(output_layer_numbers_2, output_layer_numbers_com, commas_2, bra_left_2_3, bra_right_2_3, bra_left_2_2, bra_right_2_2, text_func_2, commas, bra_left_2, bra_right_2)
        )
        self.wait()


class ConveyerBeltVariables_eng(MovingCameraScene):
    def construct(self):

        self.camera.background_color = WHITE

        d_buffer = 1

        # text_input = Tex(r"\texttt{Input-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        # text_hl = Tex(r"\texttt{Hidden-Layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        # text_output = Tex(r"\texttt{Output-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        # text_hl_2 = Tex(r"(", r"100", r" \ \texttt{neurons})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        text_input = Tex(r"\texttt{Input layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        text_hl = Tex(r"\texttt{Hidden layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        text_output = Tex(r"\texttt{Output layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        text_hl_2 = Tex(r"(", r"100", r" \ \texttt{neurons})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        d1 = config["frame_height"]/2 - text_input.get_bottom()[1]

        input_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(9)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        input_layer_2 = input_layer_1.copy()

        dots = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.4)

        input_layer = VGroup(
            input_layer_1, dots, input_layer_2
        ).arrange(DOWN, buff=0.4).set_x(-config["frame_width"]/4 - d_buffer).set_y(-d1/2)

        hidden_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(7)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        dots_2 = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.2)
        
        hidden_layer = VGroup(
            hidden_layer_1, dots_2, hidden_layer_1.copy()
        ).arrange(DOWN, buff=0.2).set_y(-d1/2)

        output_layer = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(10)]
        ).arrange(DOWN, buff=0.2).scale(0.13).set_x(config["frame_width"]/4 + d_buffer).set_y(-d1/2)

        brace_input = Brace(input_layer, LEFT).set_color(BLACK)
        brace_input_text = brace_input.get_tex(r"784").set_color(BLACK)

        brace_output = Brace(output_layer, RIGHT).set_color(BLACK)
        brace_output_text = brace_output.get_tex(r"10").set_color(BLACK)

        lines = VGroup()
        hidden_layer_neurons = VGroup(*hidden_layer[0], *hidden_layer[-1])

        for j in [0,2]:
            for k in range(9):
                lines_k = VGroup(
                    *[Line(input_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in hidden_layer_neurons]
                )

                lines.add(lines_k)

        lines_2 = VGroup()

        for j in [0,2]:
            for k in range(7):
                lines_k = VGroup(
                    *[Line(hidden_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in output_layer]
                )

                lines_2.add(lines_k)

        self.add(
            input_layer, hidden_layer, output_layer, text_input, text_hl, text_hl_2, text_output, brace_input, brace_input_text, brace_output, brace_output_text, lines, lines_2
        )
        self.wait()

        self.play(
            self.camera.frame.animate.scale(0.4).move_to(input_layer[0].get_center()+2.3*RIGHT)
        )
        self.wait()

        self.play(
            VGroup(
                input_layer[1], hidden_layer[1], text_input, text_hl, text_hl_2, text_output, brace_input, brace_input_text, brace_output, brace_output_text, lines, lines_2
            ).animate.set_opacity(0.2),
            VGroup(
                input_layer[0], input_layer[-1], hidden_layer[0], hidden_layer[-1], output_layer,
            ).animate.set_style(stroke_opacity=0.2),
            input_layer[0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),
            input_layer[-1].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),

        )
        self.wait()

        input_numbers = VGroup(
            *[
                MathTex(
                    "a^{(0)}"+"_{}".format(k),
                    color=BLACK
                ).scale(0.25).move_to(input_layer[0][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(9)
            ]
        )

        self.play(
            FadeIn(input_numbers)
        )
        self.wait()

        first_lines = VGroup(
            *[lines[k][0] for k in range(18)]
        )

        self.play(
            lines.animate.set_opacity(0.1),
        )
        self.play(
            hidden_layer[0][0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),
            first_lines.animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            )
        )
        self.wait()

        self.play(
            *[
                input_numbers[k].animate.move_to(first_lines[k].point_from_proportion(0.175))
                for k in range(9)
            ]
        )
        self.wait()

        m_dots = VGroup(
            *[
                
                Dot(
                    color=BLACK
                ).scale(0.12).next_to(input_numbers[k], RIGHT, buff=0.03).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        weight_equations = VGroup(
            *[
                MathTex(
                    "w^{(0)}"+"_{}".format(k),
                    color=RED_E,
                ).scale(0.25).next_to(m_dots[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )


        self.play(
            FadeIn(m_dots),
            FadeIn(weight_equations)
        )
        self.wait()

        text_weights = Tex(r"\texttt{Weights}").scale(0.4).set_color(RED_E).next_to(weight_equations, UP, buff=0.15)

        self.play(
            LaggedStart(
                FadeIn(text_weights),
                Circumscribe(weight_equations, color=RED_E, buff=0.02, time_width=2, run_time=3, stroke_width=2),
                lag_ratio=0.5
            )
        )
        self.wait()

        middle_numbers = VGroup(
            *[
                VGroup(
                    input_numbers[k],
                    m_dots[k],
                    weight_equations[k]
                )
                for k in range(9)
            ]
        )

        middle_numbers_2 = VGroup(
            *[
                VGroup(
                    MathTex(
                        "a^{(0)}" + "_{" + "{}".format(k+775) + "}",
                        color=BLACK
                    ).scale(0.25),
                    Dot(
                        color=BLACK
                    ).scale(0.12),
                    MathTex(
                        "w^{(0)}" + "_{" + "{}".format(k+775) + "}",
                        color=RED_E,
                    ).scale(0.25)
                ).arrange(RIGHT, buff=0.03).move_to(first_lines[k+9].point_from_proportion(0.3)).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(9)
            ]
        )

        self.add(middle_numbers_2)


        self.play(
            FadeOut(
                text_weights
            )
        )
        self.play(
            *[
                middle_numbers[k].animate.move_to(first_lines[k].point_from_proportion(0.99)).scale(0.5)
                for k in range(9)
            ],
            *[
                middle_numbers_2[k].animate.move_to(first_lines[k+9].point_from_proportion(0.99)).scale(0.5)
                for k in range(9)
            ],
            self.camera.frame.animate.set_x(2),
            run_time=2
        )

        dots_eq = VGroup(
            *[Dot(color=BLACK).scale(0.075) for _ in range(3)]
        ).arrange(RIGHT, buff=0.04).move_to(hidden_layer[0][0].get_left())


        self.remove(
            middle_numbers[3]
        )
        self.remove(
            middle_numbers[4]
        )
        self.remove(
            middle_numbers[5]
        )
        self.remove(
            middle_numbers[6]
        )
        self.remove(
            middle_numbers[7]
        )
        self.remove(
            middle_numbers[8]
        )
        self.remove(
            middle_numbers_2[0]
        )
        self.remove(
            middle_numbers_2[1]
        )
        self.remove(
            middle_numbers_2[2]
        )
        self.remove(
            middle_numbers_2[3]
        )
        self.remove(
            middle_numbers_2[4]
        )
        self.remove(
            middle_numbers_2[5]
        )

        sum_group = VGroup(
            *[middle_numbers[k] for k in range(3)],
            dots_eq,
            *[middle_numbers_2[k] for k in range(6,9)]
        )

        sum_group_aux = sum_group.copy()
        sum_group_aux.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.3*UP + 2*RIGHT)
        pluses = VGroup(
            *[
                MathTex("+").set_color(BLACK).scale(0.3).move_to(
                    sum_group_aux[k].get_right() + 0.5 * (sum_group_aux[k+1].get_left() - sum_group_aux[k].get_right())
                )
                for k in range(6)
            ]
        )


        self.play(
            sum_group.animate.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.3*UP + 2*RIGHT), #.align_to(hidden_layer[0][0], 2*UP+2*LEFT)
            # sum_group[5].animate.set_color(BLACK),
            FadeIn(pluses) 
        )

        brace_sum = Brace(sum_group, UP, stroke_width=0.2, buff=0.03).set_color(BLACK).stretch_to_fit_height(0.1)
        brace_sum_text = brace_sum.get_tex(r"784 \ \texttt{summands}").set_color(BLACK).scale(0.4).next_to(brace_sum, UP, buff=0.1)

        self.play(
            FadeIn(
                brace_sum, brace_sum_text
            )
        )

        self.wait()

        bias_num = MathTex(
            "+", "b^{(1)}_0",
            color=RED_E
        ).scale(0.25).next_to(sum_group_aux, RIGHT, buff=0.05)

        self.play(
            ReplacementTransform(
                hidden_layer[0][0].copy(),
                bias_num
            )
        )

        text_bias = Tex(r"\texttt{Bias}").scale(0.4).set_color(RED_E).next_to(bias_num[1], UP, buff=0.15)

        self.play(
            FadeIn(text_bias)
        )

        self.wait()

        bra_left = MathTex("(").set_color(DARK_BROWN).scale(0.5).next_to(sum_group_aux, LEFT, buff=0.03)
        bra_right = MathTex(")").set_color(DARK_BROWN).scale(0.5).next_to(bias_num, RIGHT, buff=0.03)

        text_func = MathTex(r"\varphi_{0}^{(1)}").scale(0.3).set_color(DARK_BROWN).next_to(bra_left, LEFT, buff=0.05) ######################### HERE

        self.play(
            FadeIn(
                bra_left, bra_right, text_func
            )
        )
        self.wait()

        hidden_input_num = MathTex(
            "=", "a^{(1)}_0",
        ).set_color(BLACK).scale(0.25).next_to(sum_group[4], DOWN, buff=0.15)

        self.play(
            FadeIn(hidden_input_num)
        )
        self.wait()

        hidden_layer_inputs_1 = VGroup(
            *[
                MathTex(
                    "a^{(1)}"+"_{}".format(k),
                    color=BLACK,
                ).scale(0.25).move_to(hidden_layer[0][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )
        hidden_layer_inputs_2 = VGroup(
            *[
                MathTex(
                    "a^{(1)}" + "_{" + "{}".format(k+93) + "}",
                    color=BLACK,
                ).scale(0.25).move_to(hidden_layer[-1][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )

        self.play(
            #hidden_input_num[1].copy().animate.scale(0.8).move_to(hidden_layer[0][0].get_center())
            ReplacementTransform(
                hidden_input_num[1].copy(),
                hidden_layer_inputs_1[0]
            )
        )
        self.wait()


        self.play(
            LaggedStart(
                FadeOut(
                    sum_group, hidden_input_num, text_func, text_bias, pluses, bra_left, bra_right, bias_num, brace_sum, brace_sum_text
                ),
                self.camera.frame.animate.scale(2.25).move_to(hidden_layer.get_center()),
                lag_ratio=0.5
            )
        )
        self.wait()

        lines_aux = lines.copy()
        lines_aux.set_color(GREEN_E).set_opacity(1)

        solo_lines = VGroup()

        for group in lines_aux:
            for line in group:
                solo_lines.add(line)

        self.play(
            *[
                Create(line) for line in solo_lines
            ]
        )

        for line in solo_lines:
            line.reverse_points()

        first_lines.set_color(BLACK).set_opacity(0.1)

        self.play(
            *[
                Uncreate(line) for line in solo_lines
            ],
            VGroup(
                hidden_layer[0], hidden_layer[-1],
            ).animate.set_style(stroke_color=GREEN_E, stroke_opacity=1),
            VGroup(
                input_layer[0], input_layer[-1],
            ).animate.set_style(stroke_color=BLACK, stroke_opacity=0.2),
            FadeIn(
                hidden_layer_inputs_1[1:], hidden_layer_inputs_2
            )
            # rate_func = lambda t: smooth(t)
        )
        self.wait(2)

        first_lines_2 = VGroup(
            *[lines_2[k][0] for k in range(14)]
        )

        self.play(
            self.camera.frame.animate.scale(0.4).shift(RIGHT*2.25).set_y(hidden_layer[0].get_y()),
            lines_2.animate.set_opacity(0.1)
        )
        self.play(
            first_lines_2.animate.set_opacity(1).set_color(GREEN_E),
            output_layer[0].animate.set_stroke(color=GREEN_E, opacity=1),
        )
        self.wait()

        ################################################################################################################################


        self.play(
            *[
                hidden_layer_inputs_1[k].animate.move_to(first_lines_2[k].point_from_proportion(0.175))
                for k in range(7)
            ]
        )
        self.wait()

        m_dots_2 = VGroup(
            *[
                Dot(
                    color=BLACK
                ).scale(0.12).next_to(hidden_layer_inputs_1[k], RIGHT, buff=0.03).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        weight_equations_2 = VGroup(
            *[
                MathTex(
                    "w^{(1)}"+"_{}".format(k),
                    color=RED_E,
                ).scale(0.25).next_to(m_dots_2[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )


        self.play(
            FadeIn(m_dots_2),
            FadeIn(weight_equations_2)
        )
        self.wait()

        text_weights_2 = Tex(r"\texttt{Weights}").scale(0.4).set_color(RED_E).next_to(weight_equations_2, UP, buff=0.15)

        self.play(
            LaggedStart(
                FadeIn(text_weights_2),
                Circumscribe(weight_equations_2, color=RED_E, buff=0.02, time_width=2, run_time=3, stroke_width=2),
                lag_ratio=0.5
            )
        )
        self.wait()


        # middle_numbers_2 = VGroup(
        #     *[
        #         DecimalNumber(
        #             hidden_layer_inputs_vals[k]*weight_values_2[k],
        #             num_decimal_places=1,
        #             color=BLACK
        #         ).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE)
        #         for k in range(7)
        #     ]
        # )


        # middle_numbers_2_2 = VGroup(
        #     *[
        #         DecimalNumber(
        #             middle_numbers_2_2_vals[k],
        #             num_decimal_places=1,
        #             color=BLACK
        #         ).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE).move_to(first_lines_2[k+7].point_from_proportion(0.175))
        #         for k in range(7)
        #     ]
        # )
        # self.add(middle_numbers_2_2)

        middle_numbers_2 = VGroup(
            *[
                VGroup(
                    hidden_layer_inputs_1[k],
                    m_dots_2[k],
                    weight_equations_2[k]
                )
                for k in range(7)
            ]
        )

        middle_numbers_2_2 = VGroup(
            *[
                VGroup(
                    MathTex(
                        "a^{(1)}" + "_{" + "{}".format(k+93) + "}",
                        color=BLACK
                    ).scale(0.25),
                    Dot(
                        color=BLACK
                    ).scale(0.12),
                    MathTex(
                        "w^{(1)}" + "_{" + "{}".format(k+93) + "}",
                        color=RED_E,
                    ).scale(0.25)
                ).arrange(RIGHT, buff=0.03).move_to(first_lines_2[k+7].point_from_proportion(0.3)).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )
        self.add(middle_numbers_2_2)


        self.play(
            FadeOut(
                text_weights_2
            )
        )
        self.play(
            *[
                middle_numbers_2[k].animate.move_to(first_lines_2[k].point_from_proportion(0.99)).scale(0.2)
                for k in range(7)
            ],
            *[
                middle_numbers_2_2[k].animate.move_to(first_lines_2[k+7].point_from_proportion(0.99)).scale(0.2)
                for k in range(7)
            ],
            run_time=1
        )
        #self.wait()

        dots_eq_2 = VGroup(
            *[Dot(color=BLACK).scale(0.03) for _ in range(3)]
        ).arrange(RIGHT, buff=0.01).move_to(output_layer[0].get_left())

        self.remove(
            middle_numbers_2[2]
        )
        self.remove(
            middle_numbers_2[3]
        )
        self.remove(
            middle_numbers_2[4]
        )
        self.remove(
            middle_numbers_2[5]
        )
        self.remove(
            middle_numbers_2[6]
        )
        self.remove(
            middle_numbers_2_2[0]
        )
        self.remove(
            middle_numbers_2_2[1]
        )
        self.remove(
            middle_numbers_2_2[2]
        )
        self.remove(
            middle_numbers_2_2[3]
        )
        self.remove(
            middle_numbers_2_2[4]
        )


        sum_group_2 = VGroup(
            *[middle_numbers_2[k] for k in range(2)],
            dots_eq_2,
            *[middle_numbers_2_2[k] for k in range(5,7)]
        )

        sum_group_aux_2 = sum_group_2.copy()
        sum_group_aux_2.scale(7).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.1*UP + 2.4*RIGHT)
        pluses_2 = VGroup(
            *[
                MathTex("+").set_color(BLACK).scale(0.3).move_to(
                    sum_group_aux_2[k].get_right() + 0.5 * (sum_group_aux_2[k+1].get_left() - sum_group_aux_2[k].get_right())
                )
                for k in range(4)
            ]
        )

        self.play(
            sum_group_2.animate.scale(7).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.1*UP + 2.4*RIGHT), #.align_to(hidden_layer[0][0], 2*UP+2*LEFT)
            # sum_group[5].animate.set_color(BLACK),
            FadeIn(pluses_2) 
        )

        brace_sum_2 = Brace(sum_group_2, UP, stroke_width=0.2, buff=0).set_color(BLACK).stretch_to_fit_height(0.1).shift(DOWN*0.05)
        brace_sum_text_2 = brace_sum_2.get_tex(r"100 \ \texttt{summands}").set_color(BLACK).scale(0.4).next_to(brace_sum_2, UP, buff=0.1)

        self.play(
            FadeIn(
                brace_sum_2, brace_sum_text_2
            )
        )

        self.wait()

        bias_num_2 = MathTex(
            "+", "b^{(2)}_0",
            color=RED_E
        ).scale(0.35).next_to(sum_group_aux_2, RIGHT, buff=0.05)

        self.play(
            ReplacementTransform(
                output_layer[0][0].copy(),
                bias_num_2
            )
        )

        text_bias_2 = Tex(r"\texttt{Bias}").scale(0.4).set_color(RED_E).next_to(bias_num_2[1], UP, buff=0.15)

        self.play(
            FadeIn(text_bias_2),
            FadeOut(hidden_layer_inputs_2)
        )

        self.wait()

        bra_left_2 = MathTex("(").set_color(DARK_BROWN).scale(0.5).next_to(sum_group_aux_2, LEFT, buff=0.05)
        bra_right_2 = MathTex(")").set_color(DARK_BROWN).scale(0.5).next_to(bias_num_2, RIGHT, buff=0.03)

        text_func_2 = MathTex(r"\varphi^{(2)}").scale(0.4).set_color(DARK_BROWN).next_to(bra_left_2, LEFT, buff=0.05)

        self.play(
            FadeIn(
                bra_left_2, bra_right_2, text_func_2
            )
        )
        self.wait()

        hidden_input_num_2 = MathTex(
            "=", "a^{(2)}_0",
        ).set_color(BLACK).scale(0.45).next_to(sum_group_2[4], DOWN, buff=0.25)

        self.play(
            FadeIn(hidden_input_num_2)
        )
        self.wait()

        self.play(
            hidden_input_num_2[1].copy().animate.scale(0.6).move_to(output_layer[0].get_center())
        )
        self.wait()

        self.play(
            LaggedStart(
                FadeOut(
                    sum_group_2, hidden_input_num_2, text_func_2, text_bias_2, pluses_2, bra_left_2, bra_right_2, bias_num_2, brace_sum_2, brace_sum_text_2
                ),
                self.camera.frame.animate.scale(2.25).move_to(hidden_layer.get_center()),
                lag_ratio=0.5
            )
        )
        self.wait()

        lines_aux_2 = lines_2.copy()
        lines_aux_2.set_color(GREEN_E).set_opacity(1)

        solo_lines_2 = VGroup()

        for group in lines_aux_2:
            for line in group:
                solo_lines_2.add(line)

        self.play(
            *[
                Create(line) for line in solo_lines_2
            ]
        )

        for line in solo_lines_2:
            line.reverse_points()

        first_lines_2.set_color(BLACK).set_opacity(0.1)

        output_layer_numbers = VGroup(
            *[
                MathTex(
                    "a^{(2)}_{" + "{}".format(k+1) + "}",
                    color=BLACK,
                ).scale(0.25).move_to(output_layer[k+1].get_center())
                for k in range(9)
            ]
        )

        self.play(
            *[
                Uncreate(line) for line in solo_lines_2
            ],
            output_layer.animate.set_style(stroke_color=GREEN_E, stroke_opacity=1),
            VGroup(
                hidden_layer[0], hidden_layer[-1],
            ).animate.set_style(stroke_color=BLACK, stroke_opacity=0.2),
            FadeIn(
                output_layer_numbers
            )
            # rate_func = lambda t: smooth(t)
        )
        self.wait()


class ConveyerBeltVariables_eng_v2(MovingCameraScene):
    def construct(self):

        self.camera.background_color = WHITE

        d_buffer = 1

        # text_input = Tex(r"\texttt{Input-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        # text_hl = Tex(r"\texttt{Hidden-Layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        # text_output = Tex(r"\texttt{Output-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        # text_hl_2 = Tex(r"(", r"100", r" \ \texttt{neurons})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        text_input = Tex(r"\texttt{Input layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        text_hl = Tex(r"\texttt{Hidden layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        text_output = Tex(r"\texttt{Output layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        text_hl_2 = Tex(r"(", r"100", r" \ \texttt{neurons})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        d1 = config["frame_height"]/2 - text_input.get_bottom()[1]

        input_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(9)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        input_layer_2 = input_layer_1.copy()

        dots = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.4)

        input_layer = VGroup(
            input_layer_1, dots, input_layer_2
        ).arrange(DOWN, buff=0.4).set_x(-config["frame_width"]/4 - d_buffer).set_y(-d1/2)

        hidden_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(7)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        dots_2 = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.2)
        
        hidden_layer = VGroup(
            hidden_layer_1, dots_2, hidden_layer_1.copy()
        ).arrange(DOWN, buff=0.2).set_y(-d1/2)

        output_layer = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(10)]
        ).arrange(DOWN, buff=0.2).scale(0.13).set_x(config["frame_width"]/4 + d_buffer).set_y(-d1/2)

        brace_input = Brace(input_layer, LEFT).set_color(BLACK)
        brace_input_text = brace_input.get_tex(r"784").set_color(BLACK)

        brace_output = Brace(output_layer, RIGHT).set_color(BLACK)
        brace_output_text = brace_output.get_tex(r"10").set_color(BLACK)

        lines = VGroup()
        hidden_layer_neurons = VGroup(*hidden_layer[0], *hidden_layer[-1])

        for j in [0,2]:
            for k in range(9):
                lines_k = VGroup(
                    *[Line(input_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in hidden_layer_neurons]
                )

                lines.add(lines_k)

        lines_2 = VGroup()

        for j in [0,2]:
            for k in range(7):
                lines_k = VGroup(
                    *[Line(hidden_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in output_layer]
                )

                lines_2.add(lines_k)

        self.add(
            input_layer, hidden_layer, output_layer, text_input, text_hl, text_hl_2, text_output, brace_input, brace_input_text, brace_output, brace_output_text, lines, lines_2
        )
        self.wait()

        self.play(
            self.camera.frame.animate.scale(0.4).move_to(input_layer[0].get_center()+2.3*RIGHT)
        )
        self.wait()

        self.play(
            VGroup(
                input_layer[1], hidden_layer[1], text_input, text_hl, text_hl_2, text_output, brace_input, brace_input_text, brace_output, brace_output_text, lines, lines_2
            ).animate.set_opacity(0.2),
            VGroup(
                input_layer[0], input_layer[-1], hidden_layer[0], hidden_layer[-1], output_layer,
            ).animate.set_style(stroke_opacity=0.2),
            input_layer[0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),
            input_layer[-1].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),

        )
        self.wait()

        input_numbers = VGroup(
            *[
                MathTex(
                    "a^{(0)}"+"_{}".format(k),
                    color=BLACK
                ).scale(0.25).move_to(input_layer[0][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(9)
            ]
        )

        self.play(
            FadeIn(input_numbers)
        )
        self.wait()

        first_lines = VGroup(
            *[lines[k][0] for k in range(18)]
        )

        self.play(
            lines.animate.set_opacity(0.1),
        )
        self.play(
            hidden_layer[0][0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),
            first_lines.animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            )
        )
        self.wait()

        self.play(
            *[
                input_numbers[k].animate.move_to(first_lines[k].point_from_proportion(0.175))
                for k in range(9)
            ]
        )
        self.wait()

        m_dots = VGroup(
            *[
                
                Dot(
                    color=BLACK
                ).scale(0.12).next_to(input_numbers[k], RIGHT, buff=0.03).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        weight_equations = VGroup(
            *[
                MathTex(
                    "w^{(0)}"+"_{}".format(k),
                    color=RED_E,
                ).scale(0.25).next_to(m_dots[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )


        self.play(
            FadeIn(m_dots),
            FadeIn(weight_equations)
        )
        self.wait()

        text_weights = Tex(r"\texttt{Weights}").scale(0.4).set_color(RED_E).next_to(weight_equations, UP, buff=0.15)

        self.play(
            LaggedStart(
                FadeIn(text_weights),
                Circumscribe(weight_equations, color=RED_E, buff=0.02, time_width=2, run_time=3, stroke_width=2),
                lag_ratio=0.5
            )
        )
        self.wait()

        middle_numbers = VGroup(
            *[
                VGroup(
                    input_numbers[k],
                    m_dots[k],
                    weight_equations[k]
                )
                for k in range(9)
            ]
        )

        middle_numbers_2 = VGroup(
            *[
                VGroup(
                    MathTex(
                        "a^{(0)}" + "_{" + "{}".format(k+775) + "}",
                        color=BLACK
                    ).scale(0.25),
                    Dot(
                        color=BLACK
                    ).scale(0.12),
                    MathTex(
                        "w^{(0)}" + "_{" + "{}".format(k+775) + "}",
                        color=RED_E,
                    ).scale(0.25)
                ).arrange(RIGHT, buff=0.03).move_to(first_lines[k+9].point_from_proportion(0.3)).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(9)
            ]
        )

        self.add(middle_numbers_2)


        self.play(
            FadeOut(
                text_weights
            )
        )
        self.play(
            *[
                middle_numbers[k].animate.move_to(first_lines[k].point_from_proportion(0.99)).scale(0.5)
                for k in range(9)
            ],
            *[
                middle_numbers_2[k].animate.move_to(first_lines[k+9].point_from_proportion(0.99)).scale(0.5)
                for k in range(9)
            ],
            self.camera.frame.animate.set_x(2),
            run_time=2
        )

        dots_eq = VGroup(
            *[Dot(color=BLACK).scale(0.075) for _ in range(3)]
        ).arrange(RIGHT, buff=0.04).move_to(hidden_layer[0][0].get_left())


        self.remove(
            middle_numbers[3]
        )
        self.remove(
            middle_numbers[4]
        )
        self.remove(
            middle_numbers[5]
        )
        self.remove(
            middle_numbers[6]
        )
        self.remove(
            middle_numbers[7]
        )
        self.remove(
            middle_numbers[8]
        )
        self.remove(
            middle_numbers_2[0]
        )
        self.remove(
            middle_numbers_2[1]
        )
        self.remove(
            middle_numbers_2[2]
        )
        self.remove(
            middle_numbers_2[3]
        )
        self.remove(
            middle_numbers_2[4]
        )
        self.remove(
            middle_numbers_2[5]
        )

        sum_group = VGroup(
            *[middle_numbers[k] for k in range(3)],
            dots_eq,
            *[middle_numbers_2[k] for k in range(6,9)]
        )

        sum_group_aux = sum_group.copy()
        sum_group_aux.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.3*UP + 2*RIGHT)
        pluses = VGroup(
            *[
                MathTex("+").set_color(BLACK).scale(0.3).move_to(
                    sum_group_aux[k].get_right() + 0.5 * (sum_group_aux[k+1].get_left() - sum_group_aux[k].get_right())
                )
                for k in range(6)
            ]
        )


        self.play(
            sum_group.animate.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.3*UP + 2*RIGHT), #.align_to(hidden_layer[0][0], 2*UP+2*LEFT)
            # sum_group[5].animate.set_color(BLACK),
            FadeIn(pluses) 
        )

        brace_sum = Brace(sum_group, UP, stroke_width=0.2, buff=0.03).set_color(BLACK).stretch_to_fit_height(0.1)
        brace_sum_text = brace_sum.get_tex(r"784 \ \texttt{summands}").set_color(BLACK).scale(0.4).next_to(brace_sum, UP, buff=0.1)

        self.play(
            FadeIn(
                brace_sum, brace_sum_text
            )
        )

        self.wait()

        bias_num = MathTex(
            "+", "b^{(1)}_0",
            color=RED_E
        ).scale(0.25).next_to(sum_group_aux, RIGHT, buff=0.05)

        self.play(
            ReplacementTransform(
                hidden_layer[0][0].copy(),
                bias_num
            )
        )

        text_bias = Tex(r"\texttt{Bias}").scale(0.4).set_color(RED_E).next_to(bias_num[1], UP, buff=0.15)

        self.play(
            FadeIn(text_bias)
        )

        self.wait()

        bra_left = MathTex("(").set_color(DARK_BROWN).scale(0.5).next_to(sum_group_aux, LEFT, buff=0.03)
        bra_right = MathTex(")").set_color(DARK_BROWN).scale(0.5).next_to(bias_num, RIGHT, buff=0.03)

        text_func = MathTex(r"\varphi_{0}^{(1)}").scale(0.3).set_color(DARK_BROWN).next_to(bra_left, LEFT, buff=0.05) ######################### HERE

        self.play(
            FadeIn(
                bra_left, bra_right, text_func
            )
        )
        self.wait()

        hidden_input_num = MathTex(
            "=", "a^{(1)}_0",
        ).set_color(BLACK).scale(0.25).next_to(sum_group[4], DOWN, buff=0.15)

        self.play(
            FadeIn(hidden_input_num)
        )
        self.wait()

        hidden_layer_inputs_1 = VGroup(
            *[
                MathTex(
                    "a^{(1)}"+"_{}".format(k),
                    color=BLACK,
                ).scale(0.25).move_to(hidden_layer[0][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )
        hidden_layer_inputs_2 = VGroup(
            *[
                MathTex(
                    "a^{(1)}" + "_{" + "{}".format(k+93) + "}",
                    color=BLACK,
                ).scale(0.25).move_to(hidden_layer[-1][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )

        self.play(
            #hidden_input_num[1].copy().animate.scale(0.8).move_to(hidden_layer[0][0].get_center())
            ReplacementTransform(
                hidden_input_num[1].copy(),
                hidden_layer_inputs_1[0]
            )
        )
        self.wait()


        self.play(
            LaggedStart(
                FadeOut(
                    sum_group, hidden_input_num, text_func, text_bias, pluses, bra_left, bra_right, bias_num, brace_sum, brace_sum_text
                ),
                self.camera.frame.animate.scale(2.25).move_to(hidden_layer.get_center()),
                lag_ratio=0.5
            )
        )
        self.wait()

        lines_aux = lines.copy()
        lines_aux.set_color(GREEN_E).set_opacity(1)

        solo_lines = VGroup()

        for group in lines_aux:
            for line in group:
                solo_lines.add(line)

        self.play(
            *[
                Create(line) for line in solo_lines
            ]
        )

        for line in solo_lines:
            line.reverse_points()

        first_lines.set_color(BLACK).set_opacity(0.1)

        self.play(
            *[
                Uncreate(line) for line in solo_lines
            ],
            VGroup(
                hidden_layer[0], hidden_layer[-1],
            ).animate.set_style(stroke_color=GREEN_E, stroke_opacity=1),
            VGroup(
                input_layer[0], input_layer[-1],
            ).animate.set_style(stroke_color=BLACK, stroke_opacity=0.2),
            FadeIn(
                hidden_layer_inputs_1[1:], hidden_layer_inputs_2
            )
            # rate_func = lambda t: smooth(t)
        )
        self.wait(2)

        first_lines_2 = VGroup(
            *[lines_2[k][0] for k in range(14)]
        )

        self.play(
            self.camera.frame.animate.scale(0.4).shift(RIGHT*2.25).set_y(hidden_layer[0].get_y()),
            lines_2.animate.set_opacity(0.1)
        )
        self.play(
            first_lines_2.animate.set_opacity(1).set_color(GREEN_E),
            output_layer[0].animate.set_stroke(color=GREEN_E, opacity=1),
        )
        self.wait()

        ################################################################################################################################


        self.play(
            *[
                hidden_layer_inputs_1[k].animate.move_to(first_lines_2[k].point_from_proportion(0.175))
                for k in range(7)
            ]
        )
        self.wait()

        m_dots_2 = VGroup(
            *[
                Dot(
                    color=BLACK
                ).scale(0.12).next_to(hidden_layer_inputs_1[k], RIGHT, buff=0.03).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        weight_equations_2 = VGroup(
            *[
                MathTex(
                    "w^{(1)}"+"_{}".format(k),
                    color=RED_E,
                ).scale(0.25).next_to(m_dots_2[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )


        self.play(
            FadeIn(m_dots_2),
            FadeIn(weight_equations_2)
        )
        self.wait()

        text_weights_2 = Tex(r"\texttt{Weights}").scale(0.4).set_color(RED_E).next_to(weight_equations_2, UP, buff=0.15)

        self.play(
            LaggedStart(
                FadeIn(text_weights_2),
                Circumscribe(weight_equations_2, color=RED_E, buff=0.02, time_width=2, run_time=3, stroke_width=2),
                lag_ratio=0.5
            )
        )
        self.wait()


        # middle_numbers_2 = VGroup(
        #     *[
        #         DecimalNumber(
        #             hidden_layer_inputs_vals[k]*weight_values_2[k],
        #             num_decimal_places=1,
        #             color=BLACK
        #         ).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE)
        #         for k in range(7)
        #     ]
        # )


        # middle_numbers_2_2 = VGroup(
        #     *[
        #         DecimalNumber(
        #             middle_numbers_2_2_vals[k],
        #             num_decimal_places=1,
        #             color=BLACK
        #         ).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE).move_to(first_lines_2[k+7].point_from_proportion(0.175))
        #         for k in range(7)
        #     ]
        # )
        # self.add(middle_numbers_2_2)

        middle_numbers_2 = VGroup(
            *[
                VGroup(
                    hidden_layer_inputs_1[k],
                    m_dots_2[k],
                    weight_equations_2[k]
                )
                for k in range(7)
            ]
        )

        middle_numbers_2_2 = VGroup(
            *[
                VGroup(
                    MathTex(
                        "a^{(1)}" + "_{" + "{}".format(k+93) + "}",
                        color=BLACK
                    ).scale(0.25),
                    Dot(
                        color=BLACK
                    ).scale(0.12),
                    MathTex(
                        "w^{(1)}" + "_{" + "{}".format(k+93) + "}",
                        color=RED_E,
                    ).scale(0.25)
                ).arrange(RIGHT, buff=0.03).move_to(first_lines_2[k+7].point_from_proportion(0.3)).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )
        self.add(middle_numbers_2_2)


        self.play(
            FadeOut(
                text_weights_2
            )
        )
        self.play(
            *[
                middle_numbers_2[k].animate.move_to(first_lines_2[k].point_from_proportion(0.99)).scale(0.2)
                for k in range(7)
            ],
            *[
                middle_numbers_2_2[k].animate.move_to(first_lines_2[k+7].point_from_proportion(0.99)).scale(0.2)
                for k in range(7)
            ],
            run_time=1
        )
        #self.wait()

        dots_eq_2 = VGroup(
            *[Dot(color=BLACK).scale(0.03) for _ in range(3)]
        ).arrange(RIGHT, buff=0.01).move_to(output_layer[0].get_left())

        self.remove(
            middle_numbers_2[2]
        )
        self.remove(
            middle_numbers_2[3]
        )
        self.remove(
            middle_numbers_2[4]
        )
        self.remove(
            middle_numbers_2[5]
        )
        self.remove(
            middle_numbers_2[6]
        )
        self.remove(
            middle_numbers_2_2[0]
        )
        self.remove(
            middle_numbers_2_2[1]
        )
        self.remove(
            middle_numbers_2_2[2]
        )
        self.remove(
            middle_numbers_2_2[3]
        )
        self.remove(
            middle_numbers_2_2[4]
        )


        sum_group_2 = VGroup(
            *[middle_numbers_2[k] for k in range(2)],
            dots_eq_2,
            *[middle_numbers_2_2[k] for k in range(5,7)]
        )

        sum_group_aux_2 = sum_group_2.copy()
        sum_group_aux_2.scale(7).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.1*UP + 2.4*RIGHT)
        pluses_2 = VGroup(
            *[
                MathTex("+").set_color(BLACK).scale(0.3).move_to(
                    sum_group_aux_2[k].get_right() + 0.5 * (sum_group_aux_2[k+1].get_left() - sum_group_aux_2[k].get_right())
                )
                for k in range(4)
            ]
        )

        self.play(
            sum_group_2.animate.scale(7).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.1*UP + 2.4*RIGHT), #.align_to(hidden_layer[0][0], 2*UP+2*LEFT)
            # sum_group[5].animate.set_color(BLACK),
            FadeIn(pluses_2) 
        )

        brace_sum_2 = Brace(sum_group_2, UP, stroke_width=0.2, buff=0).set_color(BLACK).stretch_to_fit_height(0.1).shift(DOWN*0.05)
        brace_sum_text_2 = brace_sum_2.get_tex(r"100 \ \texttt{summands}").set_color(BLACK).scale(0.4).next_to(brace_sum_2, UP, buff=0.1)

        self.play(
            FadeIn(
                brace_sum_2, brace_sum_text_2
            )
        )

        self.wait()

        bias_num_2 = MathTex(
            "+", "b^{(2)}_0",
            color=RED_E
        ).scale(0.35).next_to(sum_group_aux_2, RIGHT, buff=0.05)

        self.play(
            ReplacementTransform(
                output_layer[0][0].copy(),
                bias_num_2
            )
        )

        text_bias_2 = Tex(r"\texttt{Bias}").scale(0.4).set_color(RED_E).next_to(bias_num_2[1], UP, buff=0.15)

        self.play(
            FadeIn(text_bias_2),
            FadeOut(hidden_layer_inputs_2)
        )

        self.wait()

        bra_left_2 = MathTex("(").set_color(DARK_BROWN).scale(0.5).next_to(sum_group_aux_2, LEFT, buff=0.05)
        bra_right_2 = MathTex(")").set_color(DARK_BROWN).scale(0.5).next_to(bias_num_2, RIGHT, buff=0.03)

        text_func_2 = MathTex(r"\varphi^{(2)}").scale(0.4).set_color(DARK_BROWN).next_to(bra_left_2, LEFT, buff=0.05)

        # self.play(
        #     FadeIn(
        #         bra_left_2, bra_right_2, text_func_2
        #     )
        # )
        # self.wait()

        hidden_input_num_2 = MathTex(
            "=", "z^{(2)}_0",
        ).set_color(BLACK).scale(0.45).next_to(sum_group_2[4], DOWN, buff=0.25)

        self.play(
            FadeIn(hidden_input_num_2)
        )
        self.wait()

        hidden_input_num_2_aux = hidden_input_num_2[1].copy()

        self.play(
            hidden_input_num_2_aux.animate.scale(0.6).move_to(output_layer[0].get_center())
        )
        self.wait()

        self.play(
            LaggedStart(
                FadeOut(
                    sum_group_2, hidden_input_num_2, text_bias_2, pluses_2, bias_num_2, brace_sum_2, brace_sum_text_2
                ),
                self.camera.frame.animate.scale(2.25).move_to(hidden_layer.get_center()),
                lag_ratio=0.5
            )
        )
        self.wait()

        lines_aux_2 = lines_2.copy()
        lines_aux_2.set_color(GREEN_E).set_opacity(1)

        solo_lines_2 = VGroup()

        for group in lines_aux_2:
            for line in group:
                solo_lines_2.add(line)

        self.play(
            *[
                Create(line) for line in solo_lines_2
            ]
        )

        for line in solo_lines_2:
            line.reverse_points()

        first_lines_2.set_color(BLACK).set_opacity(0.1)

        output_layer_numbers = VGroup(
            *[
                MathTex(
                    "z^{(2)}_{" + "{}".format(k+1) + "}",
                    color=BLACK,
                ).scale(0.25).move_to(output_layer[k+1].get_center())
                for k in range(9)
            ]
        )

        self.play(
            *[
                Uncreate(line) for line in solo_lines_2
            ],
            output_layer.animate.set_style(stroke_color=GREEN_E, stroke_opacity=1),
            VGroup(
                hidden_layer[0], hidden_layer[-1],
            ).animate.set_style(stroke_color=BLACK, stroke_opacity=0.2),
            FadeIn(
                output_layer_numbers
            )
            # rate_func = lambda t: smooth(t)
        )
        self.wait()

        output_layer_numbers_com = VGroup(
            hidden_input_num_2_aux, *output_layer_numbers
        )

        self.play(
            output_layer_numbers_com.animate.scale(2).arrange(RIGHT, buff=0.1).to_edge(UR, buff=2).shift(UP*0.75)
        )

        commas = VGroup(
            *[
                MathTex(",").scale(0.7).next_to(output_layer_numbers_com[i], buff=-0.1).shift(DOWN*output_layer_numbers_com.get_height()*0.4)
                for i in range(9)
            ]
        ).set_color(BLACK)

        bra_left_2 = MathTex("[").set_color(BLACK).scale(0.75).next_to(output_layer_numbers_com, LEFT, buff=0.05)
        bra_right_2 = MathTex("]").set_color(BLACK).scale(0.75).next_to(output_layer_numbers_com, RIGHT, buff=0.03)


        self.play(
            FadeIn(commas, bra_left_2, bra_right_2)
        )
        self.wait(0.5)

        bra_left_2_2 = MathTex("(").set_color(DARK_BROWN).scale(1).next_to(bra_left_2, LEFT, buff=0.05)
        bra_right_2_2 = MathTex(")").set_color(DARK_BROWN).scale(1).next_to(bra_right_2, RIGHT, buff=0.05)
        text_func_2 = MathTex(r"\varphi^{(2)}").scale(0.8).set_color(DARK_BROWN).next_to(bra_left_2_2, LEFT, buff=0.05)

        self.play(
            FadeIn(bra_left_2_2, bra_right_2_2, text_func_2)
        )
        self.wait()

        output_layer_numbers_2 = VGroup(
            *[
                MathTex(
                    "a^{(2)}_{" + "{}".format(k) + "}",
                    color=BLACK,
                ).scale(0.5)
                for k in range(10)
            ]
        ).arrange(RIGHT, buff=0.1).next_to(output_layer_numbers_com, DOWN).to_edge(RIGHT, buff=1.75)
        commas_2 = VGroup(
            *[
                MathTex(",").scale(0.7).next_to(output_layer_numbers_2[i], buff=-0.1).shift(DOWN*output_layer_numbers_2.get_height()*0.4)
                for i in range(9)
            ]
        ).set_color(BLACK)
        bra_left_2_3 = MathTex("=[").set_color(BLACK).scale(0.75).next_to(output_layer_numbers_2, LEFT, buff=0.05)
        bra_right_2_3 = MathTex("]").set_color(BLACK).scale(0.75).next_to(output_layer_numbers_2, RIGHT, buff=0.03)


        self.play(
            FadeIn(output_layer_numbers_2, commas_2, bra_left_2_3, bra_right_2_3)
        )
        self.wait()

        self.play(
            *[
                output_layer_numbers_2[i].copy().animate.scale(0.5).move_to(output_layer[i].get_center())
                for i in range(10)
            ]
        )
        self.wait()

        self.play(
            FadeOut(output_layer_numbers_2, output_layer_numbers_com, commas_2, bra_left_2_3, bra_right_2_3, bra_left_2_2, bra_right_2_2, text_func_2, commas, bra_left_2, bra_right_2)
        )
        self.wait()


class ConveyerBeltVariables_ger_v2(MovingCameraScene):
    def construct(self):

        self.camera.background_color = WHITE

        d_buffer = 1

        # text_input = Tex(r"\texttt{Input-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        # text_hl = Tex(r"\texttt{Hidden-Layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        # text_output = Tex(r"\texttt{Output-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        # text_hl_2 = Tex(r"(", r"100", r" \ \texttt{neurons})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        text_input = Tex(r"\texttt{Input-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(-config["frame_width"]/4 - d_buffer)
        text_hl = Tex(r"\texttt{Hidden-Layer}").set_color(BLACK).to_edge(UP, buff=0.2)
        text_output = Tex(r"\texttt{Output-Layer}").set_color(BLACK).to_edge(UP, buff=0.2).set_x(config["frame_width"]/4 + d_buffer)

        text_hl_2 = Tex(r"(", r"100", r" \ \texttt{Neuronen})").set_color(BLACK).scale(0.6).next_to(text_hl, DOWN)

        d1 = config["frame_height"]/2 - text_input.get_bottom()[1]

        input_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(9)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        input_layer_2 = input_layer_1.copy()

        dots = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.4)

        input_layer = VGroup(
            input_layer_1, dots, input_layer_2
        ).arrange(DOWN, buff=0.4).set_x(-config["frame_width"]/4 - d_buffer).set_y(-d1/2)

        hidden_layer_1 = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(7)]
        ).arrange(DOWN, buff=0.15).scale(0.13)

        dots_2 = VGroup(
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
            Dot(color=BLACK).scale(0.6),
        ).arrange(DOWN, buff=0.2)
        
        hidden_layer = VGroup(
            hidden_layer_1, dots_2, hidden_layer_1.copy()
        ).arrange(DOWN, buff=0.2).set_y(-d1/2)

        output_layer = VGroup(
            *[Circle().set_style(
            fill_opacity=0,
            fill_color=BLACK,
            stroke_color=BLACK,
            stroke_width=2,
            ) for _ in range(10)]
        ).arrange(DOWN, buff=0.2).scale(0.13).set_x(config["frame_width"]/4 + d_buffer).set_y(-d1/2)

        brace_input = Brace(input_layer, LEFT).set_color(BLACK)
        brace_input_text = brace_input.get_tex(r"784").set_color(BLACK)

        brace_output = Brace(output_layer, RIGHT).set_color(BLACK)
        brace_output_text = brace_output.get_tex(r"10").set_color(BLACK)

        lines = VGroup()
        hidden_layer_neurons = VGroup(*hidden_layer[0], *hidden_layer[-1])

        for j in [0,2]:
            for k in range(9):
                lines_k = VGroup(
                    *[Line(input_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in hidden_layer_neurons]
                )

                lines.add(lines_k)

        lines_2 = VGroup()

        for j in [0,2]:
            for k in range(7):
                lines_k = VGroup(
                    *[Line(hidden_layer[j][k].get_right(), neuron.get_left()).set_style(
                        stroke_color=BLACK,
                        fill_color=BLACK,
                        stroke_width=1,
                        stroke_opacity=0.7
                    )
                    for neuron in output_layer]
                )

                lines_2.add(lines_k)

        self.add(
            input_layer, hidden_layer, output_layer, text_input, text_hl, text_hl_2, text_output, brace_input, brace_input_text, brace_output, brace_output_text, lines, lines_2
        )
        self.wait()

        self.play(
            self.camera.frame.animate.scale(0.4).move_to(input_layer[0].get_center()+2.3*RIGHT)
        )
        self.wait()

        self.play(
            VGroup(
                input_layer[1], hidden_layer[1], text_input, text_hl, text_hl_2, text_output, brace_input, brace_input_text, brace_output, brace_output_text, lines, lines_2
            ).animate.set_opacity(0.2),
            VGroup(
                input_layer[0], input_layer[-1], hidden_layer[0], hidden_layer[-1], output_layer,
            ).animate.set_style(stroke_opacity=0.2),
            input_layer[0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),
            input_layer[-1].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),

        )
        self.wait()

        input_numbers = VGroup(
            *[
                MathTex(
                    "a^{(0)}"+"_{}".format(k),
                    color=BLACK
                ).scale(0.25).move_to(input_layer[0][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(9)
            ]
        )

        self.play(
            FadeIn(input_numbers)
        )
        self.wait()

        first_lines = VGroup(
            *[lines[k][0] for k in range(18)]
        )

        self.play(
            lines.animate.set_opacity(0.1),
        )
        self.play(
            hidden_layer[0][0].animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            ),
            first_lines.animate.set_style(
                stroke_color=GREEN_E,
                stroke_opacity=1
            )
        )
        self.wait()

        self.play(
            *[
                input_numbers[k].animate.move_to(first_lines[k].point_from_proportion(0.175))
                for k in range(9)
            ]
        )
        self.wait()

        m_dots = VGroup(
            *[
                
                Dot(
                    color=BLACK
                ).scale(0.12).next_to(input_numbers[k], RIGHT, buff=0.03).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )

        weight_equations = VGroup(
            *[
                MathTex(
                    "w^{(0)}"+"_{}".format(k),
                    color=RED_E,
                ).scale(0.25).next_to(m_dots[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(9)
            ]
        )


        self.play(
            FadeIn(m_dots),
            FadeIn(weight_equations)
        )
        self.wait()

        text_weights = Tex(r"\texttt{Gewichte}").scale(0.4).set_color(RED_E).next_to(weight_equations, UP, buff=0.15)

        self.play(
            LaggedStart(
                FadeIn(text_weights),
                Circumscribe(weight_equations, color=RED_E, buff=0.02, time_width=2, run_time=3, stroke_width=2),
                lag_ratio=0.5
            )
        )
        self.wait()

        middle_numbers = VGroup(
            *[
                VGroup(
                    input_numbers[k],
                    m_dots[k],
                    weight_equations[k]
                )
                for k in range(9)
            ]
        )

        middle_numbers_2 = VGroup(
            *[
                VGroup(
                    MathTex(
                        "a^{(0)}" + "_{" + "{}".format(k+775) + "}",
                        color=BLACK
                    ).scale(0.25),
                    Dot(
                        color=BLACK
                    ).scale(0.12),
                    MathTex(
                        "w^{(0)}" + "_{" + "{}".format(k+775) + "}",
                        color=RED_E,
                    ).scale(0.25)
                ).arrange(RIGHT, buff=0.03).move_to(first_lines[k+9].point_from_proportion(0.3)).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(9)
            ]
        )

        self.add(middle_numbers_2)


        self.play(
            FadeOut(
                text_weights
            )
        )
        self.play(
            *[
                middle_numbers[k].animate.move_to(first_lines[k].point_from_proportion(0.99)).scale(0.5)
                for k in range(9)
            ],
            *[
                middle_numbers_2[k].animate.move_to(first_lines[k+9].point_from_proportion(0.99)).scale(0.5)
                for k in range(9)
            ],
            self.camera.frame.animate.set_x(2),
            run_time=2
        )

        dots_eq = VGroup(
            *[Dot(color=BLACK).scale(0.075) for _ in range(3)]
        ).arrange(RIGHT, buff=0.04).move_to(hidden_layer[0][0].get_left())


        self.remove(
            middle_numbers[3]
        )
        self.remove(
            middle_numbers[4]
        )
        self.remove(
            middle_numbers[5]
        )
        self.remove(
            middle_numbers[6]
        )
        self.remove(
            middle_numbers[7]
        )
        self.remove(
            middle_numbers[8]
        )
        self.remove(
            middle_numbers_2[0]
        )
        self.remove(
            middle_numbers_2[1]
        )
        self.remove(
            middle_numbers_2[2]
        )
        self.remove(
            middle_numbers_2[3]
        )
        self.remove(
            middle_numbers_2[4]
        )
        self.remove(
            middle_numbers_2[5]
        )

        sum_group = VGroup(
            *[middle_numbers[k] for k in range(3)],
            dots_eq,
            *[middle_numbers_2[k] for k in range(6,9)]
        )

        sum_group_aux = sum_group.copy()
        sum_group_aux.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.3*UP + 2*RIGHT)
        pluses = VGroup(
            *[
                MathTex("+").set_color(BLACK).scale(0.3).move_to(
                    sum_group_aux[k].get_right() + 0.5 * (sum_group_aux[k+1].get_left() - sum_group_aux[k].get_right())
                )
                for k in range(6)
            ]
        )


        self.play(
            sum_group.animate.scale(2.25).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.3*UP + 2*RIGHT), #.align_to(hidden_layer[0][0], 2*UP+2*LEFT)
            # sum_group[5].animate.set_color(BLACK),
            FadeIn(pluses) 
        )

        brace_sum = Brace(sum_group, UP, stroke_width=0.2, buff=0.03).set_color(BLACK).stretch_to_fit_height(0.1)
        brace_sum_text = brace_sum.get_tex(r"784 \ \texttt{Summanden}").set_color(BLACK).scale(0.4).next_to(brace_sum, UP, buff=0.1)

        self.play(
            FadeIn(
                brace_sum, brace_sum_text
            )
        )

        self.wait()

        bias_num = MathTex(
            "+", "b^{(1)}_0",
            color=RED_E
        ).scale(0.25).next_to(sum_group_aux, RIGHT, buff=0.05)

        self.play(
            ReplacementTransform(
                hidden_layer[0][0].copy(),
                bias_num
            )
        )

        text_bias = Tex(r"\texttt{Bias}").scale(0.4).set_color(RED_E).next_to(bias_num[1], UP, buff=0.15)

        self.play(
            FadeIn(text_bias)
        )

        self.wait()

        bra_left = MathTex("(").set_color(DARK_BROWN).scale(0.5).next_to(sum_group_aux, LEFT, buff=0.03)
        bra_right = MathTex(")").set_color(DARK_BROWN).scale(0.5).next_to(bias_num, RIGHT, buff=0.03)

        text_func = MathTex(r"\varphi_{0}^{(1)}").scale(0.3).set_color(DARK_BROWN).next_to(bra_left, LEFT, buff=0.05) ######################### HERE

        self.play(
            FadeIn(
                bra_left, bra_right, text_func
            )
        )
        self.wait()

        hidden_input_num = MathTex(
            "=", "a^{(1)}_0",
        ).set_color(BLACK).scale(0.25).next_to(sum_group[4], DOWN, buff=0.15)

        self.play(
            FadeIn(hidden_input_num)
        )
        self.wait()

        hidden_layer_inputs_1 = VGroup(
            *[
                MathTex(
                    "a^{(1)}"+"_{}".format(k),
                    color=BLACK,
                ).scale(0.25).move_to(hidden_layer[0][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )
        hidden_layer_inputs_2 = VGroup(
            *[
                MathTex(
                    "a^{(1)}" + "_{" + "{}".format(k+93) + "}",
                    color=BLACK,
                ).scale(0.25).move_to(hidden_layer[-1][k].get_center()).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )

        self.play(
            #hidden_input_num[1].copy().animate.scale(0.8).move_to(hidden_layer[0][0].get_center())
            ReplacementTransform(
                hidden_input_num[1].copy(),
                hidden_layer_inputs_1[0]
            )
        )
        self.wait()


        self.play(
            LaggedStart(
                FadeOut(
                    sum_group, hidden_input_num, text_func, text_bias, pluses, bra_left, bra_right, bias_num, brace_sum, brace_sum_text
                ),
                self.camera.frame.animate.scale(2.25).move_to(hidden_layer.get_center()),
                lag_ratio=0.5
            )
        )
        self.wait()

        lines_aux = lines.copy()
        lines_aux.set_color(GREEN_E).set_opacity(1)

        solo_lines = VGroup()

        for group in lines_aux:
            for line in group:
                solo_lines.add(line)

        self.play(
            *[
                Create(line) for line in solo_lines
            ]
        )

        for line in solo_lines:
            line.reverse_points()

        first_lines.set_color(BLACK).set_opacity(0.1)

        self.play(
            *[
                Uncreate(line) for line in solo_lines
            ],
            VGroup(
                hidden_layer[0], hidden_layer[-1],
            ).animate.set_style(stroke_color=GREEN_E, stroke_opacity=1),
            VGroup(
                input_layer[0], input_layer[-1],
            ).animate.set_style(stroke_color=BLACK, stroke_opacity=0.2),
            FadeIn(
                hidden_layer_inputs_1[1:], hidden_layer_inputs_2
            )
            # rate_func = lambda t: smooth(t)
        )
        self.wait(2)

        first_lines_2 = VGroup(
            *[lines_2[k][0] for k in range(14)]
        )

        self.play(
            self.camera.frame.animate.scale(0.4).shift(RIGHT*2.25).set_y(hidden_layer[0].get_y()),
            lines_2.animate.set_opacity(0.1)
        )
        self.play(
            first_lines_2.animate.set_opacity(1).set_color(GREEN_E),
            output_layer[0].animate.set_stroke(color=GREEN_E, opacity=1),
        )
        self.wait()

        ################################################################################################################################


        self.play(
            *[
                hidden_layer_inputs_1[k].animate.move_to(first_lines_2[k].point_from_proportion(0.175))
                for k in range(7)
            ]
        )
        self.wait()

        m_dots_2 = VGroup(
            *[
                Dot(
                    color=BLACK
                ).scale(0.12).next_to(hidden_layer_inputs_1[k], RIGHT, buff=0.03).set_z_index(1).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )

        weight_equations_2 = VGroup(
            *[
                MathTex(
                    "w^{(1)}"+"_{}".format(k),
                    color=RED_E,
                ).scale(0.25).next_to(m_dots_2[k], RIGHT, buff=0.03).add_background_rectangle(color=WHITE)
                for k in range(7)
            ]
        )


        self.play(
            FadeIn(m_dots_2),
            FadeIn(weight_equations_2)
        )
        self.wait()

        text_weights_2 = Tex(r"\texttt{Gewichte}").scale(0.4).set_color(RED_E).next_to(weight_equations_2, UP, buff=0.15)

        self.play(
            LaggedStart(
                FadeIn(text_weights_2),
                Circumscribe(weight_equations_2, color=RED_E, buff=0.02, time_width=2, run_time=3, stroke_width=2),
                lag_ratio=0.5
            )
        )
        self.wait()


        # middle_numbers_2 = VGroup(
        #     *[
        #         DecimalNumber(
        #             hidden_layer_inputs_vals[k]*weight_values_2[k],
        #             num_decimal_places=1,
        #             color=BLACK
        #         ).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE)
        #         for k in range(7)
        #     ]
        # )


        # middle_numbers_2_2 = VGroup(
        #     *[
        #         DecimalNumber(
        #             middle_numbers_2_2_vals[k],
        #             num_decimal_places=1,
        #             color=BLACK
        #         ).scale(0.3).set_z_index(1).add_background_rectangle(color=WHITE).move_to(first_lines_2[k+7].point_from_proportion(0.175))
        #         for k in range(7)
        #     ]
        # )
        # self.add(middle_numbers_2_2)

        middle_numbers_2 = VGroup(
            *[
                VGroup(
                    hidden_layer_inputs_1[k],
                    m_dots_2[k],
                    weight_equations_2[k]
                )
                for k in range(7)
            ]
        )

        middle_numbers_2_2 = VGroup(
            *[
                VGroup(
                    MathTex(
                        "a^{(1)}" + "_{" + "{}".format(k+93) + "}",
                        color=BLACK
                    ).scale(0.25),
                    Dot(
                        color=BLACK
                    ).scale(0.12),
                    MathTex(
                        "w^{(1)}" + "_{" + "{}".format(k+93) + "}",
                        color=RED_E,
                    ).scale(0.25)
                ).arrange(RIGHT, buff=0.03).move_to(first_lines_2[k+7].point_from_proportion(0.3)).add_background_rectangle(color=WHITE).set_z_index(1)
                for k in range(7)
            ]
        )
        self.add(middle_numbers_2_2)


        self.play(
            FadeOut(
                text_weights_2
            )
        )
        self.play(
            *[
                middle_numbers_2[k].animate.move_to(first_lines_2[k].point_from_proportion(0.99)).scale(0.2)
                for k in range(7)
            ],
            *[
                middle_numbers_2_2[k].animate.move_to(first_lines_2[k+7].point_from_proportion(0.99)).scale(0.2)
                for k in range(7)
            ],
            run_time=1
        )
        #self.wait()

        dots_eq_2 = VGroup(
            *[Dot(color=BLACK).scale(0.03) for _ in range(3)]
        ).arrange(RIGHT, buff=0.01).move_to(output_layer[0].get_left())

        self.remove(
            middle_numbers_2[2]
        )
        self.remove(
            middle_numbers_2[3]
        )
        self.remove(
            middle_numbers_2[4]
        )
        self.remove(
            middle_numbers_2[5]
        )
        self.remove(
            middle_numbers_2[6]
        )
        self.remove(
            middle_numbers_2_2[0]
        )
        self.remove(
            middle_numbers_2_2[1]
        )
        self.remove(
            middle_numbers_2_2[2]
        )
        self.remove(
            middle_numbers_2_2[3]
        )
        self.remove(
            middle_numbers_2_2[4]
        )


        sum_group_2 = VGroup(
            *[middle_numbers_2[k] for k in range(2)],
            dots_eq_2,
            *[middle_numbers_2_2[k] for k in range(5,7)]
        )

        sum_group_aux_2 = sum_group_2.copy()
        sum_group_aux_2.scale(7).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.1*UP + 2.4*RIGHT)
        pluses_2 = VGroup(
            *[
                MathTex("+").set_color(BLACK).scale(0.3).move_to(
                    sum_group_aux_2[k].get_right() + 0.5 * (sum_group_aux_2[k+1].get_left() - sum_group_aux_2[k].get_right())
                )
                for k in range(4)
            ]
        )

        self.play(
            sum_group_2.animate.scale(7).arrange(RIGHT, buff=0.15).move_to(hidden_layer[0][0].get_center() + 0.1*UP + 2.4*RIGHT), #.align_to(hidden_layer[0][0], 2*UP+2*LEFT)
            # sum_group[5].animate.set_color(BLACK),
            FadeIn(pluses_2) 
        )

        brace_sum_2 = Brace(sum_group_2, UP, stroke_width=0.2, buff=0).set_color(BLACK).stretch_to_fit_height(0.1).shift(DOWN*0.05)
        brace_sum_text_2 = brace_sum_2.get_tex(r"100 \ \texttt{Summanden}").set_color(BLACK).scale(0.4).next_to(brace_sum_2, UP, buff=0.1)

        self.play(
            FadeIn(
                brace_sum_2, brace_sum_text_2
            )
        )

        self.wait()

        bias_num_2 = MathTex(
            "+", "b^{(2)}_0",
            color=RED_E
        ).scale(0.35).next_to(sum_group_aux_2, RIGHT, buff=0.05)

        self.play(
            ReplacementTransform(
                output_layer[0][0].copy(),
                bias_num_2
            )
        )

        text_bias_2 = Tex(r"\texttt{Bias}").scale(0.4).set_color(RED_E).next_to(bias_num_2[1], UP, buff=0.15)

        self.play(
            FadeIn(text_bias_2),
            FadeOut(hidden_layer_inputs_2)
        )

        self.wait()

        bra_left_2 = MathTex("(").set_color(DARK_BROWN).scale(0.5).next_to(sum_group_aux_2, LEFT, buff=0.05)
        bra_right_2 = MathTex(")").set_color(DARK_BROWN).scale(0.5).next_to(bias_num_2, RIGHT, buff=0.03)

        text_func_2 = MathTex(r"\varphi^{(2)}").scale(0.4).set_color(DARK_BROWN).next_to(bra_left_2, LEFT, buff=0.05)

        # self.play(
        #     FadeIn(
        #         bra_left_2, bra_right_2, text_func_2
        #     )
        # )
        # self.wait()

        hidden_input_num_2 = MathTex(
            "=", "z^{(2)}_0",
        ).set_color(BLACK).scale(0.45).next_to(sum_group_2[4], DOWN, buff=0.25)

        self.play(
            FadeIn(hidden_input_num_2)
        )
        self.wait()

        hidden_input_num_2_aux = hidden_input_num_2[1].copy()

        self.play(
            hidden_input_num_2_aux.animate.scale(0.6).move_to(output_layer[0].get_center())
        )
        self.wait()

        self.play(
            LaggedStart(
                FadeOut(
                    sum_group_2, hidden_input_num_2, text_bias_2, pluses_2, bias_num_2, brace_sum_2, brace_sum_text_2
                ),
                self.camera.frame.animate.scale(2.25).move_to(hidden_layer.get_center()),
                lag_ratio=0.5
            )
        )
        self.wait()

        lines_aux_2 = lines_2.copy()
        lines_aux_2.set_color(GREEN_E).set_opacity(1)

        solo_lines_2 = VGroup()

        for group in lines_aux_2:
            for line in group:
                solo_lines_2.add(line)

        self.play(
            *[
                Create(line) for line in solo_lines_2
            ]
        )

        for line in solo_lines_2:
            line.reverse_points()

        first_lines_2.set_color(BLACK).set_opacity(0.1)

        output_layer_numbers = VGroup(
            *[
                MathTex(
                    "z^{(2)}_{" + "{}".format(k+1) + "}",
                    color=BLACK,
                ).scale(0.25).move_to(output_layer[k+1].get_center())
                for k in range(9)
            ]
        )

        self.play(
            *[
                Uncreate(line) for line in solo_lines_2
            ],
            output_layer.animate.set_style(stroke_color=GREEN_E, stroke_opacity=1),
            VGroup(
                hidden_layer[0], hidden_layer[-1],
            ).animate.set_style(stroke_color=BLACK, stroke_opacity=0.2),
            FadeIn(
                output_layer_numbers
            )
            # rate_func = lambda t: smooth(t)
        )
        self.wait()

        output_layer_numbers_com = VGroup(
            hidden_input_num_2_aux, *output_layer_numbers
        )

        self.play(
            output_layer_numbers_com.animate.scale(2).arrange(RIGHT, buff=0.1).to_edge(UR, buff=2).shift(UP*0.75)
        )

        commas = VGroup(
            *[
                MathTex(",").scale(0.7).next_to(output_layer_numbers_com[i], buff=-0.1).shift(DOWN*output_layer_numbers_com.get_height()*0.4)
                for i in range(9)
            ]
        ).set_color(BLACK)

        bra_left_2 = MathTex("[").set_color(BLACK).scale(0.75).next_to(output_layer_numbers_com, LEFT, buff=0.05)
        bra_right_2 = MathTex("]").set_color(BLACK).scale(0.75).next_to(output_layer_numbers_com, RIGHT, buff=0.03)


        self.play(
            FadeIn(commas, bra_left_2, bra_right_2)
        )
        self.wait(0.5)

        bra_left_2_2 = MathTex("(").set_color(DARK_BROWN).scale(1).next_to(bra_left_2, LEFT, buff=0.05)
        bra_right_2_2 = MathTex(")").set_color(DARK_BROWN).scale(1).next_to(bra_right_2, RIGHT, buff=0.05)
        text_func_2 = MathTex(r"\varphi^{(2)}").scale(0.8).set_color(DARK_BROWN).next_to(bra_left_2_2, LEFT, buff=0.05)

        self.play(
            FadeIn(bra_left_2_2, bra_right_2_2, text_func_2)
        )
        self.wait()

        output_layer_numbers_2 = VGroup(
            *[
                MathTex(
                    "a^{(2)}_{" + "{}".format(k) + "}",
                    color=BLACK,
                ).scale(0.5)
                for k in range(10)
            ]
        ).arrange(RIGHT, buff=0.1).next_to(output_layer_numbers_com, DOWN).to_edge(RIGHT, buff=1.75)
        commas_2 = VGroup(
            *[
                MathTex(",").scale(0.7).next_to(output_layer_numbers_2[i], buff=-0.1).shift(DOWN*output_layer_numbers_2.get_height()*0.4)
                for i in range(9)
            ]
        ).set_color(BLACK)
        bra_left_2_3 = MathTex("=[").set_color(BLACK).scale(0.75).next_to(output_layer_numbers_2, LEFT, buff=0.05)
        bra_right_2_3 = MathTex("]").set_color(BLACK).scale(0.75).next_to(output_layer_numbers_2, RIGHT, buff=0.03)


        self.play(
            FadeIn(output_layer_numbers_2, commas_2, bra_left_2_3, bra_right_2_3)
        )
        self.wait()

        self.play(
            *[
                output_layer_numbers_2[i].copy().animate.scale(0.5).move_to(output_layer[i].get_center())
                for i in range(10)
            ]
        )
        self.wait()

        self.play(
            FadeOut(output_layer_numbers_2, output_layer_numbers_com, commas_2, bra_left_2_3, bra_right_2_3, bra_left_2_2, bra_right_2_2, text_func_2, commas, bra_left_2, bra_right_2)
        )
        self.wait()