import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class ButtonSample2 {
    public static void main(String[] args) {
        Runnable runner = new Runnable() {
            public void run() {
                JFrame frame = new JFrame("Button Sample2");
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                JButton button = new JButton("Select Me");

                // define ActionListener
                ActionListener actionListener = new ActionListener() {
                    public void actionPerformed(ActionEvent actionEvent) {
                        System.out.println("I was selected");
                    }
                };

                // define MouseListener
                MouseListener mouseListener = new MouseAdapter() {
                    public void mousePressed(MouseEvent mouseEvent) {
                        int modifiers = mouseEvent.getModifiers();

                        if ((modifiers & InputEvent.BUTTON1_MASK) == InputEvent.BUTTON1_MASK) {
                            System.out.println("Left button pressed");
                        }

                        if ((modifiers & InputEvent.BUTTON2_MASK) == InputEvent.BUTTON2_MASK) {
                            System.out.println("Middle button pressed");
                        }

                        if ((modifiers & InputEvent.BUTTON3_MASK) == InputEvent.BUTTON3_MASK) {
                            System.out.println("Right button pressed");
                        }
                    }

                    public void mouseReleased(MouseEvent mouseEvent) {
                        if (SwingUtilities.isLeftMouseButton(mouseEvent)) {
                            System.out.println("Left button released");
                        }

                        if (SwingUtilities.isMiddleMouseButton(mouseEvent)) {
                            System.out.println("Middle button released");
                        }

                        if (SwingUtilities.isRightMouseButton(mouseEvent)) {
                            System.out.println("Right button released");
                        }

                        System.out.println();
                    }
                };

                // attach listener
                button.addActionListener(actionListener);
                button.addMouseListener(mouseListener);

                frame.add(button, BorderLayout.SOUTH);
                frame.setSize(300, 100);
                frame.setVisible(true);
            }
        };

        EventQueue.invokeLater(runner);
    }
}
