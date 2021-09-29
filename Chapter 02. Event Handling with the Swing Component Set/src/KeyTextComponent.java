import java.awt.*;
import java.awt.event.*;
import java.security.Key;
import javax.swing.*;

public class KeyTextComponent extends JComponent {
    private ActionListener actionListenerList = null;

    public KeyTextComponent() {
        setBackground(Color.RED);
        KeyListener internalKeyListener = new KeyAdapter() {
            public void keyPressed(KeyEvent keyEvent) {
                if (actionListenerList != null) {
                    int keyCode = keyEvent.getKeyCode();
                    String keyText = KeyEvent.getKeyText(keyCode);
                    ActionEvent actionEvent = new ActionEvent(this, ActionEvent.ACTION_PERFORMED, keyText);
                    actionListenerList.actionPerformed(actionEvent);
                }
            }
        };

        MouseListener internalMouseListener = new MouseAdapter() {
            public void mousePressed(MouseEvent mouseEvent) {
                requestFocusInWindow();
            }
        };

        addKeyListener(internalKeyListener);
        addMouseListener(internalMouseListener);
    }

    public void addActionListener(ActionListener actionListener) {
        actionListenerList = AWTEventMulticaster.add(actionListenerList, actionListener);
    }

    public void removeActionListener(ActionListener actionListener) {
        actionListenerList = AWTEventMulticaster.remove(actionListenerList, actionListener);
    }

    public boolean isFocusable() {
        return true;
    }

    public static void main(String[] args) {
        Runnable runner = new Runnable() {
            public void run() {
                JFrame frame = new JFrame("Key Text Sample");
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                KeyTextComponent keyTextComponent = new KeyTextComponent();
                final JTextField textField = new JTextField();

                ActionListener actionListener = new ActionListener() {
                    public void actionPerformed(ActionEvent actionEvent) {
                        String keyText = actionEvent.getActionCommand();
                        textField.setText(keyText);
                    }
                };

                keyTextComponent.addActionListener(actionListener);

                frame.add(keyTextComponent, BorderLayout.CENTER);
                frame.add(textField, BorderLayout.SOUTH);
                frame.setSize(300, 200);
                frame.setVisible(true);
            }
        };

        EventQueue.invokeLater(runner);
    }
}