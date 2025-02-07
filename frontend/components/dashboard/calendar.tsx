'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

type DayData = {
  mood: keyof typeof moodColors;
  content: string;
};

type MoodDataType = {
  [date: string]: DayData;
};

const moodData: MoodDataType = {
  '2024-03-01': { mood: '😊', content: 'Día productivo en el trabajo' },
  '2024-03-02': { mood: '😐', content: 'Día tranquilo en casa' },
  '2024-03-03': { mood: '😔', content: 'Me sentí un poco cansado' },
  '2024-03-04': { mood: '😊', content: 'Gran día con amigos' },
};

const moodColors = {
  '😊': 'bg-green-400',
  '😐': 'bg-yellow-400',
  '😔': 'bg-blue-400',
  '😤': 'bg-red-400',
};

export default function Calendar() {
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [currentMonth, setCurrentMonth] = useState(new Date());

  const getDaysInMonth = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const firstDay = new Date(year, month, 1).getDay();
    return { daysInMonth, firstDay };
  };

  const { daysInMonth, firstDay } = getDaysInMonth(currentMonth);

  const handlePrevMonth = () => {
    setCurrentMonth(new Date(currentMonth.setMonth(currentMonth.getMonth() - 1)));
  };

  const handleNextMonth = () => {
    setCurrentMonth(new Date(currentMonth.setMonth(currentMonth.getMonth() + 1)));
  };

  return (
    <Card className="h-full">
      <CardHeader className='flex flex-row items-center justify-between pb-4'>
        <CardTitle className='text-xl font-bold'>
          {currentMonth.toLocaleString('es-ES', { month: 'long', year: 'numeric' })}
        </CardTitle>
        <div className='flex gap-2'>
          <Button variant='outline' size='icon' onClick={handlePrevMonth}>
            <ChevronLeft className='h-4 w-4' />
          </Button>
          <Button variant='outline' size='icon' onClick={handleNextMonth}>
            <ChevronRight className='h-4 w-4' />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className='grid grid-cols-7 gap-1'>
          {['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'].map((day) => (
            <div key={day} className='text-center text-sm font-medium text-muted-foreground p-2'>
              {day}
            </div>
          ))}
          {Array.from({ length: firstDay }).map((_, index) => (
            <div key={`empty-${index}`} className='aspect-square' />
          ))}
          {Array.from({ length: daysInMonth }).map((_, index) => {
            const day = index + 1;
            const dateString = `2024-03-${day.toString().padStart(2, '0')}`;
            const dayData = moodData[dateString];

            return (
              <motion.div
                key={day}
                whileHover={{ scale: 1.1 }}
                className={cn(
                  'aspect-square p-1 cursor-pointer',
                  selectedDate === dateString && 'ring-2 ring-primary rounded-lg'
                )}
                onClick={() => setSelectedDate(dateString)}
              >
                <div
                  className={cn(
                    'w-full h-full rounded-lg flex items-center justify-center',
                    dayData ? moodColors[dayData.mood] : 'bg-secondary',
                    'transition-colors duration-200'
                  )}
                >
                  <span className='text-sm font-medium'>{day}</span>
                </div>
              </motion.div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}