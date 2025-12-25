//задача номер 1

public class TaskI {
    public static void main(String[] args) {
        int[] array = {1, -2, 3, 4, -5};
        double averagePositive = calculateAverageOfPositiveNumbers(array);
        System.out.println("Среднее арифметическое положительных чисел: " + averagePositive);
    }

    // Метод расчета среднего арифметического положительных чисел
    private static double calculateAverageOfPositiveNumbers(int[] array) {
        int sum = 0;
        int count = 0;
        for (int num : array) {
            if (num > 0) {
                sum += num;
                count++;
            }
        }
        return count != 0 ? (double)sum / count : Double.NaN;
    }
}





//задача номер 2

public class TaskII {
    public static void main(String[] args) {
        int[] array = {1, 2, 3, 4, 5};
        invertArray(array);
        printArray(array); // Выведет перевернутый массив
    }

    // Метод переворота массива вручную
    private static void invertArray(int[] array) {
        int left = 0;
        int right = array.length - 1;
        while (left < right) {
            // Меняем местами левый и правый элементы
            int temp = array[left];
            array[left++] = array[right];
            array[right--] = temp;
        }
    }

    // Вспомогательный метод вывода массива
    private static void printArray(int[] array) {
        for (int i : array) {
            System.out.print(i + " ");
        }
    }
}