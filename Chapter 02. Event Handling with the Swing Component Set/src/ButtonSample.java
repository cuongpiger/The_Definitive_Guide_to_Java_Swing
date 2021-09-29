import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class ButtonSample {
    public static void main(String[] args) {
        Runnable runner = new Runnable() {
            public void run() {
                JFrame frame = new JFrame("Button Sample");
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                JButton button = new JButton("Select Me");

                // define ActionListener
                ActionListener actionListener = new ActionListener() {
                    public void actionPerformed(ActionEvent actionEvent) {
                        System.out.println("I was selected");
                    }
                };

                // attach listeners
                button.addActionListener(actionListener);

                frame.add(button, BorderLayout.SOUTH);
                frame.setSize(300, 100);
                frame.setVisible(true);
            }
        };

        EventQueue.invokeLater(runner);
    }
}
