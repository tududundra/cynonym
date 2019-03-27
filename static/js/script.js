var Quiz = function(){
  var self = this;
  this.init = function(){
    self._bindEvents();
  }
  
  this.correctAnswers = [
      { question: 1, answer: 'b' },
      { question: 2, answer: 'b' },
      { question: 3, answer: 'b' },
      { question: 4, answer: 'c' },
      { question: 5, answer: 'c' },
      { question: 6, answer: 'c' },
      { question: 7, answer: 'a' },
      { question: 8, answer: 'b' },
      { question: 9, answer: 'a' },
      { question: 10, answer: 'b' },
  ]
  
  this._pickAnswer = function($answer, $answers){
    $answers.find('.quiz-answer').removeClass('active');
    $answer.addClass('active');
  }
  this._calcResult = function(){
    var numberOfCorrectAnswers = 0;
    $('ul[data-quiz-question]').each(function(i){
      var $this = $(this),
          chosenAnswer = $this.find('.quiz-answer.active').data('quiz-answer'),
          correctAnswer;
      
      for ( var j = 0; j < self.correctAnswers.length; j++ ) {
        var a = self.correctAnswers[j];
        if ( a.question == $this.data('quiz-question') ) {
          correctAnswer = a.answer;
        }
      }
      
      if ( chosenAnswer == correctAnswer ) {
        numberOfCorrectAnswers++;
        
        // highlight this as correct answer
        $this.find('.quiz-answer.active').addClass('correct');
      }
      else {
        $this.find('.quiz-answer[data-quiz-answer="'+correctAnswer+'"]').addClass('correct');
        $this.find('.quiz-answer.active').addClass('incorrect');
      }
    });
    if ( numberOfCorrectAnswers < 5 ) {
      return {code: 'bad', text: 'Плохо, попробуйте еще раз'};
    }
    else if ( numberOfCorrectAnswers > 8 ) {
      return {code: 'good', text: 'Отличный результат'};
    }
    else {
      return {code: 'mid', text: 'Хороший результат, но есть куда стремиться'};
    }
  }
  this._isComplete = function(){
    var answersComplete = 0;
    $('ul[data-quiz-question]').each(function(){
      if ( $(this).find('.quiz-answer.active').length ) {
        answersComplete++;
      }
    });
    if ( answersComplete >= 10 ) {
      return true;
    }
    else {
      return false;
    }
  }
  this._showResult = function(result){
    $('.quiz-result').addClass(result.code).html(result.text);
  }
  this._bindEvents = function(){
    $('.quiz-answer').on('click', function(){
      var $this = $(this),
          $answers = $this.closest('ul[data-quiz-question]');
      self._pickAnswer($this, $answers);
      if ( self._isComplete() ) {
        
        // scroll to answer section
        $('html, body').animate({
          scrollTop: $('.quiz-result').offset().top
        });
        
        self._showResult( self._calcResult() );
        $('.quiz-answer').off('click');
        
      }
    });
  }
}
var quiz = new Quiz();
quiz.init();